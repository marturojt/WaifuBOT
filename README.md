<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/marturojt/WaifuBOT">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Waifu telegram BOT</h3>

  <p align="center">
    Introducing the AI-powered virtual girlfriend of your dreams! This bot is personalized and engaging, and it's available 24/7. Chat with her about anything you want, and she'll always be there for you. She's secure and private, so you can be sure that your personal information is safe. Try her today and see for yourself how amazing she is!
    <br />
    <br />
    <a href="https://github.com/marturojt/WaifuBOT"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/marturojt/WaifuBOT">View Demo</a>
    ·
    <a href="https://github.com/marturojt/WaifuBOT/issues">Report Bug</a>
    ·
    <a href="https://github.com/marturojt/WaifuBOT/issues">Request Feature</a>
  </p>
</div>

<div>
    <ul>
        <li><strong>AI-powered virtual girlfriend:</strong> This bot is powered by artificial intelligence, which means that it can learn and adapt over time. This allows the bot to become more and more like a real girlfriend, as it learns your preferences and how to interact with you in a way that you enjoy.</li>
        <li><strong>Personalized and engaging:</strong> The bot is designed to be personalized and engaging. This means that it will tailor its conversation to your interests and personality. The bot will also be able to keep you entertained and engaged, with a variety of conversation topics and activities.</li>
        <li><strong>Available 24/7:</strong> The bot is available 24/7, so you can chat with it whenever you want. This makes it a great companion for those who are lonely or who want someone to talk to at any time of day.</li>
        <li><strong>Secure and private:</strong> The bot is secure and private, so you can chat with it without worrying about your personal information being shared. This makes it a safe and comfortable way to interact with a virtual girlfriend.</li>
    </ul>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

We are developing an AI-powered virtual girlfriend that is personalized, engaging, and available 24/7. Our goal is to create a companion that can provide companionship, support, and entertainment to people of all ages.

The project exists because we believe that everyone deserves to have someone to talk to, no matter how lonely they may feel. Our virtual girlfriend will be there for you whenever you need her, and she will always be there to listen.

Why the Project Exists

There are many reasons why this project exists. Here are a few of the most important ones:

- To provide companionship: Our virtual girlfriend can provide companionship to people who are lonely or who don't have anyone to talk to. She can be a friend, a confidante, or simply someone to listen to you.
- To provide support: Our virtual girlfriend can provide support to people who are going through a difficult time. She can offer words of encouragement, advice, or simply a shoulder to cry on.
- To provide entertainment: Our virtual girlfriend can provide entertainment to people who are looking for a way to relax and have fun. She can talk to you about anything, play games with you, or even just keep you company while you watch TV.

We believe that our virtual girlfriend has the potential to make a positive impact on the lives of many people. We are excited to see how she can help people connect, feel supported, and have fun.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python.org]][Python-url]  
[![Love][LoveBadge]][Python-url]

<!-- * [![React][React.js]][React-url]
* [![Vue][Vue.js]][Vue-url]
* [![Angular][Angular.io]][Angular-url]
* [![Svelte][Svelte.dev]][Svelte-url]
* [![Laravel][Laravel.com]][Laravel-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url] -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get started with your Python Telegram bot project, you will need the following:

- A Telegram account
- A Telegram bot
- Knowledge in Python
- OpenAI API key
- MySQL server

There are a lot of examples and documentation about creating a bot using the bot father ([Botfather](https://t.me/botfather))

Once you have the telegram bot key and openai key, you need to copy tje data.py.dist file and fill the file with your api keys. The connection info for MySQL server need to be in this file too.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/marturojt/WaifuBOT
   ```
2. Install NPM packages
   ```sh
   pip install logging openai aiogram aiogram-dialog sqlalchemy
   ```
3. Cop `data.py.dist` to `data.py` and enter your api keys and the database credentials
   ```python
    class DBOptions:
    """
    Database connection options class
    """

    def __init__(self, user: str, password: str, host: str, database: str):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    db_options = DBOptions(
                            user='[your username]', 
                            password='[your password]', 
                            host='[your host]', 
                            database='[your database name]'
                            )

    class APIKeys:
        """
        API connection details class
        """

        def __init__(self, telegram_key: str, telegram_name: str, openai_key: str):
            self.telegram_key = telegram_key
            self.telegram_name = telegram_name
            self.openai_key = openai_key

    api_options = APIKeys(
                            telegram_key='[your key]',
                            telegram_name='[your key]', 
                            openai_key='[your key]'
                            )
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->
## Roadmap

- [x] Create a basic bot
- [x] Set conversation history
- [ ] Set custom name for the girlfriend
- [ ] Add different personalities
- [ ] Add the capability to send photos
- [ ] Add the capability to send audios
- [ ] Multi-language Support
    - [ ] English
    - [x] Spanish

See the [open issues](https://github.com/marturojt/WaifuBOT/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Arturo Jiménez - [@_systemctl](https://twitter.com/_systemctl) - okami@freejolitos.com

WaifuBOT: [https://github.com/marturojt/WaifuBOT](https://github.com/marturojt/WaifuBOT)

<p align="right">(<a href="#readme-top">back to top</a>)</p>





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/marturojt/WaifuBOT?style=for-the-badge
[contributors-url]: https://github.com/marturojt/WaifuBOT/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/marturojt/WaifuBOT?style=for-the-badge
[forks-url]: https://github.com/marturojt/WaifuBOT/network/members
[stars-shield]: https://img.shields.io/github/stars/marturojt/WaifuBOT?style=for-the-badge
[stars-url]: https://github.com/marturojt/WaifuBOT/stargazers
[issues-shield]: https://img.shields.io/github/issues/marturojt/WaifuBOT?style=for-the-badge
[issues-url]: https://github.com/marturojt/WaifuBOT/issues
[license-shield]: https://img.shields.io/github/license/marturojt/WaifuBOT?style=for-the-badge
[license-url]: https://github.com/marturojt/WaifuBOT/blob/dev/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/marturojt
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
[Python.org]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://python.org/
[LoveBadge]: https://img.shields.io/static/v1?label=❤️&message=Love&style=for-the-badge&color=red
[Love-url]: https://freejolitos.com
