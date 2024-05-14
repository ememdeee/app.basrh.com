def reupload_function(cl, userName, url, story):
  # import moviepy.editor as mp  # Import moviepy
  # Fucntions
  def photo_reuploader(media,story,caption):
    #get image url ['thumbnail_url']
    thumbnail_url = media['thumbnail_url']

    #download image
    path = cl.photo_download_by_url(str(thumbnail_url), 'tmp')

    #get image caption ['caption_text']
    #caption = media['caption_text']

    if story==False:
      #upload post (Photo)
      media = cl.photo_upload(path, caption)
      print("Photo uploaded")
    elif story == True:
      #upload photo (Story)
      try:
          cl.photo_upload_to_story(path)
      except Exception:
          pass
      print("Story uploaded (Photo)")

  def reel_reuploader(media,story,caption):
    #get video url
    video_url = media['video_url']

    #download video
    path= cl.video_download_by_url(str(video_url), 'tmp')
    print ("PATHHHH", path)

    #get image caption ['caption_text']
    #caption = media['caption_text']

    if story==False:
      #upload video (Reel)
      cl.clip_upload(path, caption)
      print("Reel uploaded")
    elif story == True:
      #upload video (Story)
      try:
          cl.video_upload_to_story(path)
      except Exception:
          pass
      print("Story uploaded (Video)")
    elif story=="both":
        cl.clip_upload(path, caption)
        try:
            cl.video_upload_to_story(path)
        except Exception:
            pass
        print("Reel uploaded to feed and story!")

  def album_reuploader(media,caption):
    # Get urls
    resources = media['resources']
    thumbnail_urls = [entry['thumbnail_url'] for entry in resources]
    decoded_urls = [unquote(str(url)) for url in thumbnail_urls]

    #download images to temp server
    pathlist=cl.album_download_by_urls(decoded_urls, 'tmp')

    #get image caption ['caption_text']
    # caption = media['caption_text']

    #upload album images
    cl.album_upload(pathlist, caption)
    print("Album uploaded")

  def caption_formater (media, userName):
    caption = media['caption_text']  
    if "@" in caption:
      print("Caption Contain @!!, change it with our account")
      lines = caption.splitlines()
      new_lines = []
      for line in lines:
        new_line = ' '.join(word if "@" not in word else "@"+ userName for word in line.split())
        new_lines.append(new_line)
      caption = '\n'.join(new_lines)
    else:
        print("The caption does not contain '@'.")
    
    return caption
  # end of function



  #ask for input 
  # url = input("Enter the URL: ")
  # story_input = input("Is it a story? (Type 'y' for Yes or 'n' for No): ").lower()
  if story == 'y':
    story = True
  elif story == 'n':
    story = False
  elif story == 'b':
     story = "both"
  else:
    print("Invalid input. It's a story")
    story = True

  #stop apk if url empty
  # if url == "":
  #   break 
  
  # check media type

  #get id by url
  id = cl.media_pk_from_url(url)

  #check media type
  media=cl.media_info(id).dict()

  #Caption formater
  caption=caption_formater(media, userName)

  if media['media_type'] == 1:
      print("It's Photo")
      photo_reuploader(media,story,caption) # Run photo reuploader
  elif media['media_type'] == 2 and media['product_type'] == "feed":
      print("It's Video")
      reel_reuploader(media,story,caption) # Run video reuploader
  elif media['media_type'] == 2 and media['product_type'] == "igtv": #https://www.instagram.com/p/CWM9bCUD3pZ/ weird
      print("It's IGTV")
      reel_reuploader(media,story,caption) # Run IGTV reuploader
  elif media['media_type'] == 2 and media['product_type'] == "clips":
      print("It's Reel")
      reel_reuploader(media,story,caption) # Run Reel reuploader
  elif media['media_type'] == 8:
      print("It's Album")
      album_reuploader(media,caption) # Run album reuploader
  else:
      print("Unknown media type")
      # Handle unknown media type