def look_for_new_images(current_user_images, last_user_log):
    previous_images_ids = get_previous_images_ids(last_user_log)

    new_found_images = []
    for image in current_user_images:
        if image.id not in previous_images_ids:
            new_found_images.append(image)

    return new_found_images


def get_previous_images_ids(last_user_log):
    return last_user_log['images_ids'] if last_user_log else []