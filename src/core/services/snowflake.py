# Twitter's Snowflake algorithm implementation which is used to generate distributed IDs.
# https://github.com/twitter-archive/snowflake/blob/snowflake-2010/src/main/scala/com/twitter/service/snowflake/IdWorker.scala

import time

# div 64 bits
WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12

# max values
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)

# shift nums
WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS

# seq mask
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

TWITTER_EPOCH = 1288834974657


class InvalidSystemClock(Exception):
    pass


class IdWorker(object):  # pragma: no cover
    def __init__(self, datacenter_id: int, worker_id: int, sequence: int = 0) -> None:
        """
        :param datacenter_id: data center id
        :param worker_id: machine id
        :param sequence: start sequence
        """
        # sanity check
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError("worker_id overflow")

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError("datacenter_id overflow")

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # last time timestamp

    @staticmethod
    def _generate_timestamp() -> int:
        return int(time.time() * 1000)

    def get_id(self) -> int:
        timestamp = self._generate_timestamp()

        if timestamp < self.last_timestamp:
            raise InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._until_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = (
            ((timestamp - TWITTER_EPOCH) << TIMESTAMP_LEFT_SHIFT)
            | (self.datacenter_id << DATACENTER_ID_SHIFT)
            | (self.worker_id << WORKER_ID_SHIFT)
            | self.sequence
        )
        return new_id

    def _until_next_millis(self, last_timestamp: int) -> int:
        timestamp = self._generate_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._generate_timestamp()
        return timestamp


if __name__ == "__main__":
    worker = IdWorker(1, 2, 0)
    print(worker.get_id())
