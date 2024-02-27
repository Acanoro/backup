def preparing_upload_photos(photos_info):
    new_photos_info = []
    for num, photo_data in enumerate(photos_info):
        likes = photo_data['likes']
        for j, other_photo_data in enumerate(photos_info):
            if num != j:
                if other_photo_data['likes'] == likes:
                    new_photos_info.append(
                        {
                            'name': f'{photo_data["likes"]}_{photo_data["date"]}',
                            'type': photo_data['type'],
                            'link_photo': photo_data["photo"]
                        }
                    )
                    break
        else:
            new_photos_info.append(
                {
                    'name': photo_data["likes"],
                    'type': photo_data['type'],
                    'link_photo': photo_data["photo"]
                }
            )

    return new_photos_info
