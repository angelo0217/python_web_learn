import pika

class AMQPProducer():
    _instance = None
    _connection = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._connection == None:
            print('init start connection --------')
            self._connection = self._get_connection()
        elif self._connection.is_closed:
            print('start re connection --------')
            self._connection.close()
            self._connection = None
            self._connection = self._get_connection()

    @staticmethod
    def _get_connection():
        print('_get_connection ================')
        parameters = pika.ConnectionParameters('localhost', 5672)
        return pika.BlockingConnection(parameters)

    def send(self):
        self.chkConnection()
        channel = self._connection.channel()

        channel.exchange_declare(exchange='logs', durable=False, exchange_type='fanout')

        channel.basic_publish(exchange='logs'
                              , routing_key=''
                              , body='hello world!')

    def chkConnection(self):
        if self._connection.is_closed:
            print('start re connection --------')
            try:
                self._connection.close()
            except Exception as ex:
                print('close error', ex)
            self._connection = None
            self._connection = self._get_connection()

# connection.close()
