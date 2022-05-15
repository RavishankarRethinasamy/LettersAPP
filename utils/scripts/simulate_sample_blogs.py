import os
import sys
import argparse
import random
from string import ascii_lowercase

possible_topdir = os.path.normpath(os.path.join(
    os.path.abspath(os.path.join(sys.argv[0], os.pardir, os.pardir, os.pardir))))

if os.path.exists(os.path.join(possible_topdir, 'app', '__init__.py')):
    sys.path.insert(0, possible_topdir)

from app.api.v1.blog.actions import Blogs

parser = argparse.ArgumentParser()
parser.add_argument("--count", default=25)
parser.add_argument("--type", default='story')
parser.add_argument("--user", default="guest")

args = parser.parse_args()

sample_contents = {
    1: [
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\nHit anything about fashion, product reviews, "
                      "cinema, lifestyle, parenting, political, technology, AI, news, literature etc...\n\nHit "
                      "anything about fashion, product reviews, cinema, lifestyle, parenting, political, technology, "
                      "AI, news, literature etc...\n\n\n"
        }
    ],

    2: [
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\n"
        },
        {
            "attributes": {
                "bold": True
            },
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "insert": "\n\nHit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "header": 2
            },
            "insert": "\n"
        },
        {
            "insert": "\nHit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\n\nHit anything about fashion, product reviews, "
                      "cinema, lifestyle, parenting, political, technology, AI, news, literature "
                      "etc...\n\nHit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\nHit anything about fashion, product reviews, cinema, "
                      "lifestyle, parenting, political, technology, AI, news, literature etc...\n\n\nHit anything "
                      "about fashion, product reviews, cinema, lifestyle, parenting, political, technology, "
                      "AI, news, literature etc..."
        },
        {
            "attributes": {
                "code-block": True
            },
            "insert": "\n\n"
        },
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "code-block": True
            },
            "insert": "\n\n"
        },
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "code-block": True
            },
            "insert": "\n\n"
        },
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "code-block": True
            },
            "insert": "\n"
        },
        {
            "insert": "\nHit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\nHit anything about fashion, product reviews, cinema, "
                      "lifestyle, parenting, political, technology, AI, news, literature etc...\n\n\n\n\n\n"
        }
    ],
    3: [
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\nHit anything about fashion, product reviews, "
                      "cinema, lifestyle, parenting, political, technology, AI, news, literature etc...\n\n"
        },
        {
            "attributes": {
                "height": "474.4690909090909",
                "width": "713"
            },
            "insert": {
                "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxAPEBAODxAPDw0NDw8PDg"
                         "8QDxAPEA8PFREWFxYVFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMsNygtLisBCgoKDg0OFhAPFy0dHiUt"
                         "LS8tKy4tLSstLS0tLS0tLSstLSstLS0rKy0tKy0tLS0tKy0rLS0tLS0rLS0tLS0tLf/AABEIALcBEwMBIg"
                         "ACEQEDEQH/xAAbAAACAwEBAQAAAAAAAAAAAAAAAQIDBAYFB//EADoQAAICAQMCBQIDBAkFAQAAAAECAAMRB"
                         "BIhBTEGEyJBUWFxMoGRQlKhsRQjYoLB0eHw8TNDcqKyJP/EABkBAQEBAQEBAAAAAAAAAAAAAAABAgMEBf/EA"
                         "CARAQEBAQACAwEAAwAAAAAAAAABAhEDMRIhQVEiMmH/2gAMAwEAAhEDEQA/APlOI4Rz1vmiOEYEMgCMCMCMC"
                         "E6QEliMCSAlZ6jiMCTCya1wioLJqmZctc9jw54fu11m1AVorI8+/HFY74B92x7SW8azi6vHg+XDy59U8TeEtJ/RG"
                         "s01bLdpq9+/du89VPrDD94DnIHtPm5rmc763vw3FY9kWybPLh5c11j4MeyIrNgpzwBkn2kWqjp8axlZEiazXKmrhO"
                         "WM5EgRLmWQIhZVcUmRIw30oRxSAijhClFGYQpQgYQCEBCA4RRwJRwjAlYAEkBACSAlS0ASQEYEmqQxaiqy1a5Ylc"
                         "uWuOrMqlrlq1yzAHJ7THqteBwnJ+Zlvj0el6B9VcunqIUnLW2t+Cmofidvt8e5wJ9L0F1apXpNKPL01GFBPDs+7D"
                         "WMR3znJP8AlicHqSenaavTKcanVKL9Y2BkAjNdfI7AHP3M97wrwott3Ct1AQqrlharcdv2cH2zwBOd/r1eOSXn6"
                         "7i8HydjMCXR0cHdnlGyAR/PGMGfGtnx2n1zqdyAVOfxAqXKYbgtsKNs7Dljz8CfJeraxKbraiDursdMYx2YiTHu"
                         "r5vUR8uZ9TcEwB6nJwFHeY7+qMeFG3+c6jwJ4dNzi+5c9mrBP/tN289uOc/K8j1vC/hvyx/S9SSXQbgg7Jxx9zO"
                         "X1p3WOw7M7H9TPqPiZzRpjgA54z2IM+YMszn+uvkzJJmMhSVtXNpSVsk11wuXm2pKGE9C1JjsWblctTigiRxLCJE"
                         "iCVDEJLEWIaRiksQhUTFGYpFEUcIUhAwjgKEIQLRJARCTAmnOgCTAiAlqLDFoRZoRIVpNKJJa1nKKJFfetYye/wA"
                         "Q1V2xcjGfaeLZYXOScmRtbqdUbD8D2E1+HdEL9TVWxwm8M3/ivJE80iel4eu2XKQMtggfmJnf+t46eOT5Tq/rnUD"
                         "bqrrGySbnAB9lDED+AE7Tw91SyunC1b6CvKr/AFgBx2AYEjv24nN+MqaxdVUlYRlqVrCO72MMn9Pc/JM9fo3UX0"
                         "VZrsrJsuUConcyjClh6R/ADuSe2Jm3sjrmXOr1b17xC1j11VZ2i90atxWVzWM53jnhm7+/86+qV6XVh7XCDXVFG"
                         "fuE1IyQMgc7ucZ9yo9pDpfQrWapnKlS+85K7S7jgq2OQ2T99uDgyB0yqQlHJVhm70qGxZnDFuezn2zke4xMX/jf"
                         "L+vAboZwLAreWG2OpwLEbIB+h+/1E+n+GL6wFUL5bqoABPBXHH8jOe0tFhK2A/8AbK4UndhlCq4BHLZ9scbTnmb"
                         "9HonfyWNi16qsgWruytqAANkDsc7ftnEl1dLjEx6R8a69ncVZ4HPBnKlZ0XifTOduobC7lXeAc4bHb6meGleefYd"
                         "5vN+mNz/JTs9/b+cqdZps5/wHxK2Wac7GG1ZjtWelasxWrNRz1GFhIES91lRE04oERYkjFC9RiMlEYVAyMm0jDUI"
                         "wjMUiiEIQpQjhAvEkBEJNRNONqSiaK1laCaaxFTMWVrL1EgglrYAJ+BMO0jxOpW7mwOwmVZK9ssT8mQlQMY63KkM"
                         "pwR2MQhCx7l/WWvaqx/8AqUoqlv3iCTk/rOu6X1etkqWxK8jDLncpLKc+hgMDk/lnt8fOUrbGcfP24HM1rq84BGf"
                         "2TkkenHbic9Y/jtjy2e3f63rDEFa0FbsSq1WKBvLYIyB7djnHzjucebVq2exBySwK+Y34Sn4WY499ue574PMydFv"
                         "exk21hn9LqGyVsQHkEE49JC+2eM8AToendIQuQ20B1B8t8WAOLCzKmCM/Q+xHI4nOzjvLdfcWdQwibtrG1QwoBYM"
                         "B2U9/xFSzbR8sPmbOm2Gq2gkDL1IgYqFV6xaoOO+SFrH6/SVro2GCFXYDYyl0JAWxRuUEnj1A85/hI9W0KirTakW"
                         "ErRdXRWuNqglhlTz8gnI9jxM9b5XuajQ16hH01ilQcW054K+nJHHfBnBdRpNDnTt3T3xjd/an0tK/LRH3D+rrULn"
                         "hdhAGPvuKzxfF3SjYrkAG2kCxcdyjDgH7cy51yp5MdnXDYkGEs2fMRE6vOy2iYrRPQtEx2iWMaYXEoYTXYJmcTpH"
                         "n1FRikjEZWUYjJRGRpBpCTaQhuAxRmRkWHAQhAIQhA0iWLICTWacKuSXI0zZjV4rUr0a2lfUrdqY/e4lK3heSZ5+r"
                         "1G859h2mXTqgwxCOAo8wMWYVMWkc57dpbTcQRg4IO7txx/OZ4ZgdZ4b16hq1tuWtKyQd+SpQ59O1dpx92I5PA7H2"
                         "emtrrLHqpovtVlY17kqrDKgxgWEZxwOARnOMzhOnO1braM+hhyCVI/vAcT7J0Pxkwry2bNjKtbHLKwcekZUZ7gjJ"
                         "E5bnHp8N79dcd1jresOoGmvb+gAocs/mbVUKwHpT8WW4zg+3sDmfhjxHbrMaLV4dFO4YUKxKq3Bx37mdB4wXS9QU"
                         "6mvaurRWrNVzioD1EnYzenOV7EjA3fM4Kvpur6fbVrLqx5RswXV0sTJJBBKk4PeZvx1OT21PnnXb9x9Z6F1ZNT51"
                         "QxhVKhT+6Mcn6cY4/wCKPEeov2WanTqRWXemxsAnFTFM49hkGc54O6nT/T7wrAIxLhuwbPGM/HM7mxVr0Oq2sbFZ"
                         "r7STgBN7Fiv5ZnOc7x3vbLXyxpAyZOZBp3eVRbMds22zHbLGNMbzNZNNkzWGbjhtUYozFNOYiMcUioPKjLXlZh0yU"
                         "UcUjRwijgEIo4GoSQkRJCbeemTI7oGU2t7SLJ1G18yEI5HafQjEUJEOCKCcEhfqQSPzxzCAEKCg+QfqM4P6iMJIn6"
                         "dpJXx9YGis8Yzxnt8zovDtqUMWdNwypCl3HAIIztGCMictgn/Cb9E+xgxUN24J4P37zGo3i8r6Suvq1Ppr4IBNwBr"
                         "Cp6WOCzHgYY9l7457mV1t5tbaaxAKNVTYjqe62KB5bcdmBA/Q8zkbNfqCrDd5aFMAbVUNyOw4LE454OfjE3VanUVs"
                         "1dPpeupHdNQ61sd5ACZzwcFjwR3/AE53PXpm/ty1VlumbI9LLkEHjd6uT/CfUPDWrOq0t1ikhLamS9SeEtReH/McH"
                         "7Ced1vwRqtewtpSqkqpr2G0Mp2MQCGA9xjvz3h4O0mu0On6iltS110nY4fuLnULxj8WVZT8Yk3zXL+teL5ZtzfXHl"
                         "Ef7Eg0s7SDCdHFRZMd02WTHdLGNMVsyuZotMytOkefaJhCErIiMISCDyoy15XDpkopLEUi9KEeIQpQjhA0iTEzG0y"
                         "PmGa65fCtbdpkY5MNxikrWc8OEQEYkaOEICEKMPgEe57/AG+P9/EREQEKc0U6ViN5K1p7O5wDj90DLN+QMqX4Ubm9j"
                         "jP6CbdDp97F7WyqDdZzkAYOA784yRgAZP0irFumahWC7Lb2zgLu8lWPsAq5Y/qD9J69wsTGSmm9hRpUB1BPwXJLL/"
                         "ebP9mZNNYXZqtGPJAyLLT6bCPfc/JVeDwD7H7Tpuh6eupQ+wsvIW1vS1zDhtg/YqGRlvxMSAMZInO3jrjPXO63QbS"
                         "LrQUY87Wtzb/eY8bzg8AcdyBPY6Z04XFqHW1VtWtnFmpQ+UATgF8bucrxjjd956+q6I13/wCl62Nn4dONuVqz2bHb"
                         "PwPoPpOk8KdFWpgihvR6rHbvZa34nYnueP5TNrrPHevd6H0taNxRK697ZdwXJc7mOTnAz6u4Hf7ReK9TV5FtI5LsH"
                         "vNe3epwNpI+fSP0mHxx4jSmnyKWzc52syn8A+84KnqbCwWEklhstzzvH1kmW7v8UdSrIIbghuzDs3+swkzTqbMFlH4"
                         "Sc4+JjYzbjULDMdxmqwzFcZY56Y7jMrS+0zOZ0jz69lCEUIcIoQqLyuTeQhuJSBk5AwQxFAQkUQhCAoQhCnCKOACO"
                         "KOEBhJLLEpZvwhm/8QTCKRJN8Adv4/UyRpYHBBGPY8cyVXPAUsx4H298fXtC8PS0b8lm2Vr+IgZY/CqP2mP+pwJsq"
                         "qa3CgeXSo3KgP7PvY5x27Zcj6Ae02aPSafHNmyxbCFsbmusBhwB+0547cf4e2NBsxa4JrsZXrQMptYtn1aodtv7qjP"
                         "6ZJxdcdc+Prza6FbAYbaceYSv/cTOTYy5yEzjA7scZ9sd14P6ZZqLDbapFOFGnU9ggHpH5d/jJMxdC06OWFoqfGbHN"
                         "yLVb6f39uMAfIGBj4nY9M1tf9WwVqzjA8sm2ooO2WHB+/17zhrfXrx4+Oh0owvlkDK/THM8PxZqzVSdpKn5Xgz1D1S"
                         "ncFLAMeBuBXP2M83xGAamxzwT3klasfJ9Rflickk9yfeVo8h1Gz1nHEpptnoeLv2122Z5lRMRMgTC9KwzFcZpczJaZ"
                         "YxqslsoMutlJm3n/UYoGKFOKEUKGkJJpGGociZKRMLAIGEDIFCEIUQhCAQhCA4QhCGJNc4JyB+fJkI1+sDTpbgp5/D"
                         "jHBxwe/P/ADNK3AYbyyFZicBtpKdtu7GSPpPPY8/74l6W5YZJA+M5Hv8Ax5Jz8kyWLK1isPzWfwkBU9IIIXn1H2zj+"
                         "M9Kq6/TrvJZEvVhhW3YIUMMDPs2ff3PxMOh06MX3tt2JuBJGCVVdo/Jiv3DYmsJZXUm4Ar2XFufxEMH2dhx7/Ug/TF"
                         "dc/16mj69bWA1LhrSfXRZWqupPGUbtjjJGPf850HSurax2CKgrUEgrtRQy575zggZ7A/nObs6QuqWu+lj5q+m9UUZQ"
                         "DjJBPPtz988czsPCVasGUqRn0bgSwrZRgZU8px9SDOOufj0+P5d+66j+jIVBcKG9u2P5Tx+s6pQjIzYbGNuQf8AYnt"
                         "0V7E8p0JHswG4f5/nPN650VHRihGccqwz/GYjrXzLqNK7s8zz/wALY/Oa+pN5bEc8HGP9Z5Juycz2SfT5u7JXphpFj"
                         "KKrZJmkXoczLaZa7TNY0sY1VNhlJljmVNNuUIyMZkTI0IRQhQZGMxQ1DiMcRkBCKOFKEIQCEIQCEIQHCKOARiKOEPM"
                         "moB5PAx3+srljc8DhR3JgXWrt9IJK7Rn+0N3P8QP0ntdG14JVLONhC1M3dFIOcn3XkHH+E53fz8/ebqmTC7iwyq7vf"
                         "jew/wDnEzqfTedcrtqqHVV2N/WAFLBWQQUz+E85yAVIbPOf06TRdOPkBvOsFiAYsPpJHGQW7/rmcR0/qqoVJcvW+FN"
                         "iECxMHjeD3+/GffvPoXROq1msAsCAcHC4wQe+O4E8+s17caj1ens6AVsSxUDDE5Yj6/M0dR1KpWWOMYmSxAx31vgn3"
                         "B3KROY8b9SsSvYGHI5GMRnPau9STrjfE19ZdiuQSfic0zSy+0sSSczOTPVJx8vV+V60VXYmxbMieUGmiu2Wwl41O0z"
                         "u0bPKSYkZt6CZWYyZAmFkBkY4obEUISKDFAwgEDCIwARxRwpQhCAQhCAQhCARxQgOAhCESEPpFAQGo+Zr09DZOQHAG"
                         "cZxkDPY/lMqgfPeepRpkV08zzBUf2gPSc+4MUjX0uqksoelw3bIzhwfkexnfdC0woGa2d6TjCsM7D9+4+PynB9PsUM"
                         "EdnU1nCNnblM8c9s/Wd30PqZxsBLj3YgZ/P5nLUejxWOgbHLLgce3GT9Z8m8WdatttZHXaEJA/wCZ3nX+p+XUxXjj7"
                         "fpPkmt1DWOWY5JM1ifqefXqKy8jukY50cOHmTRpXGsiWNG6RJkQYsyscMmRMCYjDUgihFI0IQhAIoGEKcUIQCEIQC"
                         "EIQCEIQCEIQCEIQCEcIBGIQhF1VLE4Ayc4xkCenphd5ZUcoOytg4PYj7f5CEJKSPQ0t42LVauT+w4wTj4PzOk6Tikb"
                         "e+Rwe2IQkrr468XxV1AOhQEhgf1nFmOE1PTnq91ShCEIJIQhBQTEDHCUEUISBQhCAQhCFKEIQCEIQCEIQCEIQP/Z"
            }
        },
        {
            "insert": "\n\nHit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\nHit anything about fashion, product reviews, "
                      "cinema, lifestyle, parenting, political, technology, AI, news, literature etc...\n\nHit "
                      "anything about fashion, product reviews, cinema, lifestyle, parenting, political, technology"
                      ", AI, news, literature etc...\n\n\n"
        }
    ],

    4: [
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "list": "ordered"
            },
            "insert": "\n"
        },
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc.."
        },
        {
            "attributes": {
                "list": "ordered"
            },
            "insert": "\n"
        },
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "list": "ordered"
            },
            "insert": "\n"
        },
        {
            "insert": "\n\nHit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "list": "bullet"
            },
            "insert": "\n"
        },
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "list": "bullet"
            },
            "insert": "\n"
        },
        {
            "insert": "Hit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc..."
        },
        {
            "attributes": {
                "list": "bullet"
            },
            "insert": "\n"
        },
        {
            "insert": "\n\t\nHit anything about fashion, product reviews, cinema, lifestyle, parenting, political, "
                      "technology, AI, news, literature etc...\n\nHit anything about fashion, product reviews, cinema,"
                      " lifestyle, parenting, political, technology, AI, news, literature etc...\n\nHit anything "
                      "about fashion, product reviews, cinema, lifestyle, parenting, political, technology, AI, news,"
                      " literature etc...\n\n\n\n\n"
        }
    ]
}


def generate():
    print("Simulating started....")
    for ctr in range(1, int(args.count) + 1):
        sample_req = {
            "name": f"Sample {''.join(random.choices(ascii_lowercase, k=random.randint(10, 20)))} - {ctr}",
            "content": sample_contents.get(random.randint(1, 4)),
            "type": args.type
        }
        Blogs().create(sample_req, kwargs={"user_name": args.user})
    print("Simulating completed")


if __name__ == '__main__':
    generate()
