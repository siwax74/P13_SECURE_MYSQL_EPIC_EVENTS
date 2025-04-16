from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


class CRUDMixin:
    def __init__(self, session: Session):
        self.session = session

    def create(self, model, **kwargs):
        """Créer une nouvelle instance d’un modèle."""
        try:
            obj = model(**kwargs)
            self.session.add(obj)
            self.session.commit()
            print(f"✅ {model.__name__} créé avec succès.")
            return obj
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Erreur lors de la création de {model.__name__} : {e}")
            return None

    def update(self, model, obj_id, **kwargs):
        """Mettre à jour une instance existante."""
        try:
            obj = self.session.get(model, obj_id)
            if not obj:
                print(f"❌ {model.__name__} avec l'ID {obj_id} introuvable.")
                return None

            for attr, value in kwargs.items():
                if value == "":
                    continue

                setattr(obj, attr, value)

            self.session.commit()
            print(f"✅ {model.__name__} avec l'ID {obj_id} mis à jour.")
            return obj
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Erreur lors de la mise à jour de {model.__name__} : {e}")
            return None

    def delete(self, model, obj_id):
        """Supprimer une instance existante."""
        try:
            obj = self.session.get(model, obj_id)
            if not obj:
                print(f"❌ {model.__name__} avec l'ID {obj_id} introuvable.")
                return None

            self.session.delete(obj)
            self.session.commit()
            print(f"✅ {model.__name__} avec l'ID {obj_id} supprimé.")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"❌ Erreur lors de la suppression de {model.__name__} : {e}")
            return False

    def list(self, model):
        """Lister toutes les instances d’un modèle."""
        try:
            results = self.session.query(model).all()
            print(f"✅ {len(results)} instance(s) de {model.__name__} récupérée(s).")
            return results
        except SQLAlchemyError as e:
            print(f"❌ Erreur lors de la récupération de {model.__name__} : {e}")
            return []
