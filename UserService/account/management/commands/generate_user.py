import random

import requests
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.management import BaseCommand

from account.models import Account, ProfileImage


class Command(BaseCommand):
    help = 'Generates Random Person'

    def handle(self, *args, **options):
        for _ in range(1):
            # Account
            r = requests.get("https://www.fakenamegenerator.com/gen-random-au-us.php", headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
            })

            soup = BeautifulSoup(r.text, "html.parser")
            name, surname = soup.select_one(".info h3").get_text(strip=True).split(" ")

            extras = {
                dl.select_one("dt").get_text(strip=True):
                          dl.select_one("dd").get_text(strip=True, separator="###").split("###")[0]
                for dl in soup.select(".extra dl")
            }

            account = Account(
                username=extras['Username'],
                email=extras['Email Address'],
                name=name,
                surname=surname,
                phone=extras['Phone'] if random.random() > 0.6 else ""
            )
            account.set_password(extras['Email Address'].split("@")[0])
            account.save()

            # Photo
            use_photo = random.random() > 0.15
            if use_photo:
                r = requests.get(f"https://unsplash.com/napi/search/photos?query=random%20people&per_page=20&page={random.randint(1, 100)}&xp=", headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
                })
                url = random.choice(r.json()['results'])['links']['download']

                image = requests.get(url, stream=True, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
                })
                loaded = ContentFile(image.content)

                photo = ProfileImage()
                photo.set_image(InMemoryUploadedFile(
                    loaded,  # file
                    None,  # field_name
                    "image.jpg",  # file name
                    'image/jpeg',  # content_type
                    loaded.tell,  # size
                    None  # content_type_extra
                ))
                photo.owner = account
                photo.save()

                account.photo = photo.pk
                account.save()

            self.stdout.write(self.style.SUCCESS("\n-- ".join([
                "User created:",
                "Name: " + name,
                "Surname: " + surname,
                "Username: " + extras['Username'],
                "Email Address: " + extras['Email Address'],
                "Phone: " + (account.phone if account.phone != "" else "Not Set"),
                "Photo: " + str(use_photo)
            ])))
