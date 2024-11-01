from app.extensions import db


class Form(db.Model):
    __tablename__ = "form"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(7))  # formato de cor hex (#FFFFFF)
    image = db.Column(db.String(255))  # URL da imagem, se aplicável
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)

    components = db.relationship("FormComponent", backref="form", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "color": self.color,
            "image": self.image,
            "group": self.group_id,
            "components": [component.to_dict() for component in self.components],
        }

    def __repr__(self):
        return f"<Form {self.title}>"


class FormComponent(db.Model):
    __tablename__ = "form_component"

    id = db.Column(db.Integer, primary_key=True)
    form_id = db.Column(db.Integer, db.ForeignKey("form.id"), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)

    options = db.relationship("ComponentOption", backref="component", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "title": self.title,
            "options": [option.to_dict() for option in self.options],
        }

    def __repr__(self):
        return f"<FormComponent {self.title} - {self.type}>"


class ComponentOption(db.Model):
    __tablename__ = "component_option"

    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.Integer, db.ForeignKey("form_component.id"), nullable=False)
    option = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {"id": self.id, "option": self.option}

    def __repr__(self):
        return f"<ComponentOption {self.option}>"
