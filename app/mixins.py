from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.decorators import Decorator


class CRUDMixin:
    def __init__(self, session: Session):
        self.session = session

    @Decorator.safe_execution
    def create(self, model, **kwargs):
        """Créer une nouvelle instance d’un modèle."""
        obj = model(**kwargs)
        self.session.add(obj)
        self.session.commit()
        print(f"✅ Objet créé : {obj}")
        return obj

    @Decorator.safe_execution
    def update(self, model, obj_id, **kwargs):
        """Mettre à jour une instance existante."""
        obj = self.session.get(model, obj_id)
        if obj:
            for attr, value in kwargs.items():
                if value != "":
                    setattr(obj, attr, value)
            self.session.commit()
            print(f"✅ Objet mis à jour : {obj}")
            return obj
        else:
            print(f"⚠️ Aucun objet trouvé avec l'ID {obj_id}.")
            return None

    @Decorator.safe_execution
    def delete(self, model, obj_id):
        """Supprimer une instance existante."""
        obj = self.session.get(model, obj_id)
        if obj:
            self.session.delete(obj)
            self.session.commit()
            print(f"✅ Objet supprimé : {obj}")
            return obj
        else:
            print(f"⚠️ Aucun objet trouvé avec l'ID {obj_id}.")
            return None

    @Decorator.safe_execution
    def list(self, model):
        """Lister toutes les instances d’un modèle."""
        objects = self.session.query(model).all()
        return objects
