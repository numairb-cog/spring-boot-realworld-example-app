from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./dev.db"
    jwt_secret: str = "nRvyYC4soFxBdZ-F-5Nnzz5USXstR1YylsTd-mA0aKtI9HUlriGrtkf-TiuDapkLiUCogO3JOK7kwZisrHp6wA"
    jwt_session_time: int = 86400
    default_image: str = "https://static.productionready.io/images/smiley-cyrus.jpg"
    
    class Config:
        env_file = ".env"


settings = Settings()
