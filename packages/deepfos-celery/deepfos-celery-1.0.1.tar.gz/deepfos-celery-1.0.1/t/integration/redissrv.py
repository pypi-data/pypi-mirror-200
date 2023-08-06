import subprocess
import socket
import os
from tempfile import NamedTemporaryFile


def get_redis_connection(port=None):
    from redis import StrictRedis
    return StrictRedis(
        port=port
    )


class RedisServer:
    def __init__(self, redis_executable=None):
        self._serving = False
        self._proc: subprocess.Popen = None
        self._redis = redis_executable or self.find_executable('redis-server')
        self._port = self.find_available_port()

    def as_url(self):
        return f"redis://:{self.port}"

    @property
    def client(self):
        from redis import StrictRedis
        return StrictRedis(port=self.port)

    @property
    def port(self):
        return self._port

    @staticmethod
    def find_executable(exe):
        try:
            executable = subprocess.check_output(
                f"which {exe}".split(), text=True)
            return executable.strip()
        except subprocess.CalledProcessError:
            raise RuntimeError(f'exe not avaliable.')

    @staticmethod
    def find_available_port() -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("localhost", 0))
            return sock.getsockname()[1]

    def get_start_cmd(self):
        return f"nohup {self._redis} --port {self._port}".split()

    def start(self):
        if self._serving:
            return
        cmd = self.get_start_cmd()
        self._proc = subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        self._serving = True

    def stop(self):
        if not self._serving:
            return
        self._proc.terminate()
        self._proc.wait()
        self._proc = None
        self._serving = False

    def restart(self):
        self.stop()
        self.start()

    def kill_clients(self, type='all'):
        if type == 'all':
            types = ['normal', 'pubsub']
        else:
            types = [type.lower()]

        with self.client.pipeline() as pipe:
            for t in types:
                pipe.client_kill_filter(_type=t)
            pipe.execute()

    def kill_by_port(self, port):
        self.client.client_kill(f"127.0.0.1:{port}")

    def pause(self, seconds):
        self.client.client_pause(timeout=int(seconds * 1000))

    def __repr__(self):
        if self._serving:
            return f"Redis | Port: {self._port} | PID: {self._proc.pid}"
        else:
            return f"Redis | Stopped"

    def __del__(self):
        self.stop()


class RedisSentinelServer(RedisServer):
    def __init__(self, master_name: str = 'mymaster', redis_executable=None):
        super().__init__(redis_executable)
        self.master_name = master_name
        self.master = RedisServer()
        self._redis = redis_executable or self.find_executable(
            'redis-sentinel')
        self._conf = None

    def as_url(self):
        return f"sentinel://:{self.port}"

    @property
    def client(self):
        from redis.sentinel import Sentinel
        s = Sentinel([('localhost', self.port)])
        return s.master_for(self.master_name)

    def get_start_cmd(self):
        conf = self.create_configure()
        return f"nohup {self._redis} {conf.name}".split()

    def create_configure(self):
        configure = "\n".join((
            f"port {self.port}",
            f"sentinel monitor {self.master_name} localhost {self.master.port} 2",
            f"sentinel config-epoch {self.master_name} 0",
            "sentinel deny-scripts-reconfig yes"
        ))
        self._conf = f = NamedTemporaryFile(
            mode='wt', delete=False, encoding='utf8')
        f.writelines(configure)
        f.flush()
        return f

    def start(self):
        if self._serving:
            return
        self.master.start()
        super().start()

    def stop(self):
        if not self._serving:
            return

        super().stop()
        self._conf.close()
        os.unlink(self._conf.name)
        self.master.stop()
