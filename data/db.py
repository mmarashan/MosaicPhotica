import datetime
import os
import traceback
import types

from sqlalchemy import create_engine, ForeignKey, func, UniqueConstraint, Boolean
from sqlalchemy import Column, String, Integer, DateTime, JSON
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from util.file_hash import from_file_sha

Base = declarative_base()

from util.logs import get_logger
LOGGER = get_logger("ALCHEMY_DB_CLIENT")


class ImageDB(Base):
    __tablename__ = 'persona'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    date_create = Column('date_create', DateTime, default=datetime.datetime.utcnow)

    theme_tag = Column(String, index=True)  # theme
    img_path = Column(String, index=True, unique=True)
    file_hash = Column(String, index=True, unique=True)

    # value of mean-pixel
    R_mean = Column(Integer)
    G_mean = Column(Integer)
    B_mean = Column(Integer)
    CAP_mean = Column(Integer)

    def __str__(self):
        result = ''
        CALLABLES = (types.FunctionType, types.MethodType)
        for key, value in self.__dict__.items():
            if not isinstance(value, CALLABLES):
                result = result + '"' + str(key) + '":"' + str(value) + '",'
        result = '{' + result + '}'
        return result



class DBClient():
    db_string: str = 'sqlite:///images.sqlite3'
    db: Engine = None
    Session = None
    session_factory = None
    scoped_session = None

    def __init__(self):
        self.connect()

    def connect(self):
        LOGGER.info('Connect to DB')
        self.db = create_engine(self.db_string)
        Base.metadata.create_all(self.db)
        self.session_factory = sessionmaker(self.db)
        self.scoped_session = scoped_session(self.session_factory)
        LOGGER.info('Connect to DB OK')

    def get_session(self):
        # создается одна и та же сессия https://docs.sqlalchemy.org/en/latest/orm/contextual.html
        self.scoped_session = scoped_session(self.session_factory)
        session = self.scoped_session()
        return session

    def add_image(self, theme_tag:str, img_path:str,
                  R_mean:int, G_mean:int, B_mean:int, CAP_mean:int)-> ImageDB:
        LOGGER.debug("Add new image " + img_path)
        session = self.get_session()
        try:
            file_hash = from_file_sha(img_path)
            image = session.query(ImageDB)\
                .filter(ImageDB.theme_tag == theme_tag)\
                .filter(ImageDB.file_hash == file_hash)\
                .first()

            if image is not None:
                LOGGER.warning('image already exist: ' + image.img_path)
                os.remove(img_path)
                print("Image "+ img_path +"Removed!")
                return image

            image: ImageDB = ImageDB(theme_tag = theme_tag, img_path = img_path, file_hash = file_hash,
                                     R_mean = R_mean, B_mean = B_mean, G_mean = G_mean, CAP_mean = CAP_mean)
            session.add(image)
            session.flush()
            session.commit()
            LOGGER.debug("Add new image OK")
            session.close()
            return image
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            return None

    def delete_image(self, img_path: str):
        session = self.get_session()
        LOGGER.warning('Delete image ' + img_path)
        image = session.query(ImageDB) \
            .filter(ImageDB.img_path == img_path) \
            .delete()
        os.remove(img_path)
        print("Image " + img_path + "Removed!")

    def get_images(self, theme_tag:str) -> []:
        session = self.get_session()
        try:
            i = session.query(ImageDB).filter(ImageDB.theme_tag==theme_tag).all()
            session.close()
            if i is not None:
                return i
            return []
        except Exception:
            LOGGER.error(traceback.format_exc())
            return []


    def get_tags(self) -> list:
        session = self.get_session()
        try:

            tags = []
            for value in session.query(ImageDB.theme_tag).distinct():
                tags.append(value.theme_tag)

            session.close()
            return tags
        except Exception:
            LOGGER.error(traceback.format_exc())
            return []

    def get_source_path(self, theme_tag) -> str:
        session = self.get_session()
        try:
            i = session.query(ImageDB).filter(ImageDB.theme_tag == theme_tag).first()
            session.close()
            return os.path.dirname(i.img_path)
        except Exception:
            LOGGER.error(traceback.format_exc())
            return ""


    def get_nearest_by_manchetten_distance(self, theme_tag:str,
                  R_mean:int, G_mean:int, B_mean:int, CAP_mean:int)-> str:
        """
        :param theme_tag:
        :param R_mean:
        :param G_mean:
        :param B_mean:
        :param CAP_mean:
        :return: img_path
        """
        pass

    def upload_path(self, theme_tag: str, dir_path: str):
        try:
            for filename in os.listdir(dir_path):
                if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
                    self.add_image(theme_tag, dir_path+"/"+filename, 0, 0, 0, 0)

        except Exception:
            LOGGER.debug("Could not upload : " + str(dir_path))
            LOGGER.debug(str(traceback.format_exc()))
