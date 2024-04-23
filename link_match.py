import re

def extract_links(text):
  """
  This function takes a string as input and uses regular expressions to extract all the links (URLs) starting with "www" and store them in a list.

  Args:
      text: The string to extract links from.

  Returns:
      A list of all the links found in the text starting with "www".
  """
  # Regular expression pattern to match links starting with "www"
  url_pattern = r"www\.[^\s]+"
  # url_pattern_2 = r"https?://[^\s]+"

  links = re.findall(url_pattern, text)
#   links2 = re.findall(url_pattern_2, text)
#   links=links+links2
  return (links)

# Example usage
# text = """Similar video sharing platforms:

# https://www.youtube.com/ - A global video-sharing platform with a vast library of content.
# https://vimeo.com/ - A platform known for high-quality videos and a focus on creativity.
# https://www.dailymotion.com/ - Another popular video-sharing platform with a strong international presence.
# https://www.twitch.tv/ - Primarily focused on live streaming, but also offers video on demand for gaming content.
# https://d.tube/ - A decentralized video platform built on blockchain technology.
# Sites for specific content Bilibili might offer:

# https://www.crunchyroll.com/ - Popular for anime and Asian dramas.
# https://www.theverge.com/2024/2/8/24065940/funimation-shutdown-crunchyroll-digital-library - Another major streaming service for anime.
# https://www.netflix.com/ - Global streaming giant with a wide variety of shows and movies, including some anime.
# https://www.disneyplus.com/ - Home to Disney, Pixar, Marvel, Star Wars, and National Geographic content. May have some overlap with Bilibili's animation offerings.
# https://www.twitch.tv/creative - While Twitch is mainly for gaming, the Creative category features content creation tutorials and streams, similar to some Bilibili content.
# Chinese video platforms:

# https://youku.com/ - A major video platform in China with a similar interface to Bilibili.
# https://v.qq.com/ - Another large Chinese video platform owned by Tencent.
# https://m.iqiyi.com/ - A leading Chinese online video platform with a diverse library of content.
# Remember, these are just a few examples, and the best alternative for you will depend on the specific content you're looking for."""
# links = extract_links(text)

# # Print the extracted links
# print(links)
