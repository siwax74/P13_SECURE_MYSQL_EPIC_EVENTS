from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


class CRUDMixin:
    def __init__(self, session):
        self.session = session

    def create(self, model, data):
        """Créer une nouvelle instance d'un modèle."""
        try:
            instance = model(**data)
            self.session.add(instance)
            self.session.commit()
            return instance.id
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erreur lors de la création : {e}")
            return None

    def update(self, model, instance_id, data):
        """Mettre à jour une instance d'un modèle existant."""
        try:
            instance = self.session.query(model).get(instance_id)
            if not instance:
                print(f"Instance avec l'id {instance_id} non trouvée.")
                return None

            for key, value in data.items():
                setattr(instance, key, value)

            self.session.commit()
            return instance
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erreur lors de la mise à jour de l'instance : {e}")
            return None

    def delete(self, model, instance_id):
        """Supprimer une instance existante."""
        try:
            instance = self.session.query(model).get(instance_id)
            if not instance:
                print(f"Instance avec l'id {instance_id} non trouvée.")
                return None

            self.session.delete(instance)
            self.session.commit()
            print(f"Instance avec l'id {instance_id} supprimée.")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erreur lors de la suppression de l'instance : {e}")
            return False

    def list(self, model):
        """Lister toutes les instances d'un modèle."""
        try:
            return self.session.query(model).all()
        except SQLAlchemyError as e:
            print(f"Erreur lors de la récupération des données : {e}")
            return []
