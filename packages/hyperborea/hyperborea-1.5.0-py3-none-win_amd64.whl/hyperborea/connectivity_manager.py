import functools
import logging
import multiprocessing.connection
import selectors
import socket
import threading
import time

from PySide6 import QtCore

from hyperborea.preferences import read_int_setting
from hyperborea.proxy import DeviceLoggerAdapter

logger = logging.getLogger(__name__)


class BasicConnectivityHandler:
    def __init__(self):
        pass

    def stop_device(self, serial_number):
        # NOTE: any device callbacks have already been cleared
        pass

    def create_channel_callbacks(self, serial_number, channel_infos):
        return [None] * len(channel_infos)

    def stop(self):
        pass

    def join(self):
        pass

    def update_settings(self):
        pass


class SocketTransmitter:
    def __init__(self, serial_number, channel_info, ports, selector, logger):
        self.serial_number = serial_number
        self.channel_info = channel_info
        self.ports = ports
        self.selector = selector
        self.logger = logger

        self.scale = channel_info.unit_formatter.conversion_scale
        self.offset = channel_info.unit_formatter.conversion_offset

        self.listen_sockets = [None] * len(ports)
        self.connected_sockets = set()

        for subchannel_id, port in enumerate(ports):
            if not port:
                continue

            try:
                # create a TCP socket
                listen_sock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
                listen_sock.setsockopt(
                    socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                listen_sock.setblocking(False)
                listen_sock.bind(("", port))
                listen_sock.listen()

                accept_cb = functools.partial(self._accept_ready,
                                              subchannel_id)
                self.selector.register(
                    listen_sock, selectors.EVENT_READ, accept_cb)

                self.logger.info(f"Listening for connections on port {port}")

                self.listen_sockets[subchannel_id] = listen_sock
            except Exception:
                self.logger.exception("Error opening socket on port %s",
                                      port)

    def stop(self):
        self.logger.debug(f"Stopping transmitting sockets")

        for listen_sock in self.listen_sockets:
            if listen_sock:
                try:
                    self.selector.unregister(listen_sock)
                except KeyError:
                    pass  # ignure, selector must already be closed
                listen_sock.close()
        self.listen_sockets = [None] * len(self.listen_sockets)

        connected_sockets_copy = self.connected_sockets.copy()
        self.connected_sockets.clear()

        for connected_sock, _subchannel_id in connected_sockets_copy:
            try:
                self.selector.unregister(connected_sock)
            except KeyError:
                pass  # ignure, selector must already be closed

            addr = connected_sock.getsockname()
            try:
                port = addr[1]
            except Exception:
                port = "<UNKNOWN>"

            connected_sock.close()

            self.logger.info("Connection closed on %s", port)

    def callback(self, data):
        data = (data - self.offset) / self.scale
        data = data.astype("<f8")

        for sock, subchannel_id in self.connected_sockets.copy():
            socket_bytes = data[:, subchannel_id].tobytes()
            try:
                sent = sock.send(socket_bytes)
            except Exception:
                # error on this socket
                self._close_socket(sock)
                continue
            if sent != len(socket_bytes):
                # other end couldn't keep up
                self._close_socket(sock)

    def _accept_ready(self, subchannel_id):
        try:
            listen_sock = self.listen_sockets[subchannel_id]
            port = self.ports[subchannel_id]

            connected_sock, _addr = listen_sock.accept()  # Should be ready

            self.logger.info("Accepted new connection on port %s", port)

            connected_sock.setblocking(False)
            connected_sock.setsockopt(
                socket.IPPROTO_TCP, socket.TCP_NODELAY, True)

            close_cb = functools.partial(self._close_socket, connected_sock)

            # any read event means to close the socket
            self.selector.register(
                connected_sock, selectors.EVENT_READ, close_cb)

            self.connected_sockets.add((connected_sock, subchannel_id))
        except OSError:
            pass
        except Exception:
            self.logger.exception("Unhandled exception in _accept_ready()")

    def _close_socket(self, connected_sock):
        try:
            self.selector.unregister(connected_sock)
        except KeyError:
            pass  # ignure, selector must already be closed

        for socket, subchannel_id in self.connected_sockets.copy():
            if socket == connected_sock:
                self.connected_sockets.remove((socket, subchannel_id))
                break

        addr = connected_sock.getsockname()
        try:
            port = addr[1]
        except Exception:
            port = "<UNKNOWN>"

        connected_sock.close()

        self.logger.info("Connection closed on %s", port)


class SocketHandler(BasicConnectivityHandler):
    def __init__(self):
        super().__init__()

        self.settings = QtCore.QSettings()

        self.socket_transmitters = {}  # k serial, v set(socket_transmitter)
        self.device_ports = {}  # k serial, v set(ports)
        self.used_ports = set()

        self.selector = selectors.DefaultSelector()

        self.selector_thread_finished = threading.Event()
        self.selector_thread = threading.Thread(target=self._selector_loop)
        self.selector_thread.start()

    def stop(self):
        self.selector_thread_finished.set()

        for s in self.socket_transmitters.values():
            for socket_transmitter in s:
                socket_transmitter.stop()
        self.socket_transmitters.clear()
        self.device_ports.clear()

    def join(self):
        self.selector_thread.join()

    def stop_device(self, serial_number):
        s = self.socket_transmitters.get(serial_number)
        if s:
            for socket_transmitter in s:
                socket_transmitter.stop()
            s.clear()
        ports = self.device_ports.pop(serial_number, None)
        if ports:
            for port in ports:
                self.used_ports.discard(port)

    def create_channel_callbacks(self, serial_number, channel_infos):
        device_logger = DeviceLoggerAdapter(logger, serial_number)

        callbacks = [None] * len(channel_infos)
        for i, channel_info in enumerate(channel_infos):
            subchannel_count = len(channel_info.subchannel_names)
            ports = []
            for subchannel_id in range(subchannel_count):
                setting_name = "{}/Channel{}_{}_Port".format(
                    serial_number, channel_info.channel_id, subchannel_id)
                port = read_int_setting(self.settings, setting_name, None)

                if port is not None:
                    if port in self.used_ports:
                        other_device = "<UNKNOWN>"
                        for d, s in self.device_ports.items():
                            if port in s:
                                other_device = d
                                break
                        device_logger.warning("Port %s already in use by %s!",
                                              port, other_device)
                        port = None
                    else:
                        self.used_ports.add(port)
                        s = self.device_ports.setdefault(serial_number, set())
                        s.add(port)

                ports.append(port)

            if all(x is None for x in ports):
                # not interested in this channel
                continue

            socket_transmitter = SocketTransmitter(
                serial_number, channel_info, ports, self.selector,
                device_logger)
            s = self.socket_transmitters.setdefault(serial_number, set())
            s.add(socket_transmitter)

            callbacks[i] = [socket_transmitter.callback]

        return callbacks

    def _selector_loop(self):
        try:
            selector_map = self.selector.get_map()
            while not self.selector_thread_finished.is_set():
                if len(selector_map) == 0:
                    # no sockets open yet
                    time.sleep(0.1)
                else:
                    events = self.selector.select(timeout=0.1)
                    for key, _mask in events:
                        callback = key.data
                        callback()
        except Exception:
            logger.exception("Uncaught exception in selector_loop")
            self.stop()
        finally:
            self.selector.close()


class ConnectivityManager:
    def __init__(self):
        self.stopped = False

        self.pipe_lock = threading.Lock()
        self.all_pipes = []
        self.pipe_callbacks = {}  # k pipe, v set(cbs)
        self.device_pipes = {}  # k serial, v set(pipes)

        self.pipe_thread_finished = threading.Event()
        self.pipe_thread = threading.Thread(target=self._pipe_loop)
        self.pipe_thread.start()

        self.handlers = [SocketHandler()]

    def add_handler(self, handler):
        self.handlers.append(handler)

    def stop(self):
        # NOTE: the calc process may still be pushing data into pipes
        # so the pipe thread can't be stopped yet

        self.stopped = True

        # stop all handlers
        for handler in self.handlers:
            handler.stop()

        with self.pipe_lock:
            self.device_pipes.clear()
            self.pipe_callbacks.clear()

    def join(self):
        # NOTE: the calc process has been joined at this point

        # join all handlers
        for handler in self.handlers:
            handler.join()

        self.pipe_thread_finished.set()
        self.pipe_thread.join()

    def create_channel_pipes(self, serial_number, channel_infos):
        # clean up any old entries first
        self.stop_device(serial_number)

        if self.stopped:
            # we've already stopped
            return [None] * len(channel_infos)

        all_callbacks = [set() for _i in range(len(channel_infos))]

        for handler in self.handlers:
            new_callbacks = handler.create_channel_callbacks(
                serial_number, channel_infos)
            for n, cb_set in zip(new_callbacks, all_callbacks):
                if n:
                    cb_set.update(n)

        device_pipes = set()
        channel_tx_pipes = [None] * len(channel_infos)
        channel_rx_pipes = [None] * len(channel_infos)
        for i, cb_set in enumerate(all_callbacks):
            if not cb_set:
                continue

            channel_rx_pipe, channel_tx_pipe = multiprocessing.Pipe(False)
            channel_rx_pipes[i] = channel_rx_pipe
            channel_tx_pipes[i] = channel_tx_pipe
            device_pipes.add(channel_rx_pipe)

        with self.pipe_lock:
            for channel_rx_pipe, cb_set in zip(channel_rx_pipes, all_callbacks):
                if channel_rx_pipe:
                    self.pipe_callbacks[channel_rx_pipe] = cb_set
            self.device_pipes[serial_number] = device_pipes
            self.all_pipes.extend(device_pipes)

        return channel_tx_pipes

    def stop_device(self, serial_number):
        with self.pipe_lock:
            pipes = self.device_pipes.pop(serial_number, None)
            if pipes:
                for pipe in pipes:
                    self.pipe_callbacks.pop(pipe, None)

        for handler in self.handlers:
            handler.stop_device(serial_number)

    def read_settings(self):
        if self.stopped:
            # we've already stopped
            return

        for handler in self.handlers:
            handler.update_settings()

    def _remove_pipe(self, pipe):  # call with pipe_lock held
        self.all_pipes.remove(pipe)
        self.pipe_callbacks.pop(pipe, None)

        for pipe_set in self.device_pipes.values():
            pipe_set.discard(pipe)

    def _pipe_loop(self):
        try:
            while True:
                if self.pipe_thread_finished.is_set():
                    return

                with self.pipe_lock:
                    all_pipes_copy = self.all_pipes.copy()

                if not all_pipes_copy:
                    self.pipe_thread_finished.wait(0.1)
                    continue

                ready = multiprocessing.connection.wait(all_pipes_copy,
                                                        timeout=0.1)
                with self.pipe_lock:
                    for pipe in ready:
                        try:
                            data = pipe.recv()
                            if data is None:
                                # None signals that this pipe is done
                                self._remove_pipe(pipe)
                            else:
                                callbacks = self.pipe_callbacks.get(pipe)
                                if callbacks:
                                    for callback in callbacks:
                                        callback(data)
                        except EOFError:
                            self._remove_pipe(pipe)
        except Exception:
            logger.exception("Uncaught exception in pipe_loop")
            self.stop()
