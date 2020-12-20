## Anonymus Bot

Telegram bot to send messages anonymously (not forward) to your group.

## Tutorial

  - Deploy with Docker

    ~~~
    git clone https://github.com/traitcode/anonymus.git
    cd anonymus
    ~~~

    Run this after configuration 
    
    ~~~
    docker-compose -f "docker-compose.yml" up -d --build
    ~~~

  - Configurations

    - Create config.py

      ~~~
      cp config.sample.py config.py
      ~~~

    - Update Config

      ~~~
      "BOT_TOKEN": "your_token",
      "BOT_MANAGER": your_user_id,
      ~~~

  - Add bot to your group

    ~~~
    /setgroup
    ~~~

  - Send text or media to Bot

  - Enjoy


## Credit

Crax97, 91DarioDev