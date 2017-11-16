"""cloudAMQP_client_test"""
from cloud_amqp_client import CloudAMQPClient

CLOUDAMQP_URL = "amqp://awvcegnf:dJFJDov0uwTo_wMk-vvhAq_FcvznLjIR@wombat.rmq.cloudamqp.com/awvcegnf"
NEWS_FETCH_TASK_QUEUE_NAME = "test"


def test_basic():
    """basic test"""
    client = CloudAMQPClient(CLOUDAMQP_URL, NEWS_FETCH_TASK_QUEUE_NAME)

    sent_msg = {'test': 'test'}
    client.send_message(sent_msg)
    received_msg = client.get_message()
    assert sent_msg == received_msg
    print 'test_basic passed.'


if __name__ == "__main__":
    test_basic()
