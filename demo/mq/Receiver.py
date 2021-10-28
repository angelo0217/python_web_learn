import threading

import pika

class AMQPConsuming(threading.Thread):
    def callback(self, ch, method, properties, body):
        print(" [x] received %r " % body)

    @staticmethod
    def _get_connection():
        parameters = pika.ConnectionParameters('test-server', 5672)
        return pika.BlockingConnection(parameters)

    def run(self):
        connection = self._get_connection()

        channel = connection.channel()

        channel.exchange_declare(exchange='logs', durable=False, exchange_type='fanout')

        result = channel.queue_declare('', exclusive=True)

        queue_name = result.method.queue

        print("random queueName: ", queue_name)

        channel.queue_bind(exchange='logs', queue=queue_name)

        channel.basic_consume(
            queue_name,
            self.callback,
            auto_ack=True
        )

        print('当前MQ简单模式正在等待生产者往消息队列塞消息.......要退出请按 CTRL+C.......')
        channel.start_consuming()

