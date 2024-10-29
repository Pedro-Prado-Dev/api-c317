from flask import request, jsonify
from flask_restful import Resource
from app.extensions import db, api
from app.form.model import Form, FormComponent, ComponentOption


class FormResource(Resource):
    def get(self, form_id=None):
        if form_id:
            form = Form.query.get(form_id)
            if form:
                return jsonify(form.to_dict())
            return {"message": "Form not found"}, 404
        else:
            forms = Form.query.all()
            return jsonify([form.to_dict() for form in forms])

    def post(self):
        data = request.get_json()
        new_form = Form(
            title=data.get('title'),
            color=data.get('color'),
            image=data.get('image'),
            group_id=data.get('group')
        )

        for comp_data in data.get('components', []):
            component = FormComponent(
                type=comp_data['type'],
                title=comp_data['title']
            )
            for opt in comp_data.get('options', []):
                option = ComponentOption(option=opt)
                component.options.append(option)
            new_form.components.append(component)

        db.session.add(new_form)
        db.session.commit()
        return new_form.to_dict(), 201

    def put(self, form_id):
        data = request.get_json()
        form = Form.query.get(form_id)
        if not form:
            return {"message": "Form not found"}, 404

        form.title = data.get('title', form.title)
        form.color = data.get('color', form.color)
        form.image = data.get('image', form.image)
        form.group_id = data.get('group', form.group_id)

        db.session.commit()
        return form.to_dict(), 200

    def delete(self, form_id):
        form = Form.query.get(form_id)
        if not form:
            return {"message": "Form not found"}, 404
        db.session.delete(form)
        db.session.commit()
        return {"message": "Form deleted"}, 200

class FormComponentResource(Resource):
    def get(self, form_id, component_id=None):
        form = Form.query.get(form_id)
        if not form:
            return {"message": "Form not found"}, 404

        if component_id:
            component = FormComponent.query.get(component_id)
            if component and component.form_id == form_id:
                return component.to_dict()
            return {"message": "Component not found"}, 404
        else:
            return [component.to_dict() for component in form.components], 200

    def post(self, form_id):
        form = Form.query.get(form_id)
        if not form:
            return {"message": "Form not found"}, 404

        data = request.get_json()
        component = FormComponent(
            type=data['type'],
            title=data['title']
        )

        for opt in data.get('options', []):
            option = ComponentOption(option=opt)
            component.options.append(option)

        form.components.append(component)
        db.session.commit()
        return component.to_dict(), 201

    def delete(self, form_id, component_id):
        component = FormComponent.query.get(component_id)
        if not component or component.form_id != form_id:
            return {"message": "Component not found"}, 404
        db.session.delete(component)
        db.session.commit()
        return {"message": "Component deleted"}, 200


class ComponentOptionResource(Resource):
    def get(self, component_id):
        component = FormComponent.query.get(component_id)
        if not component:
            return {"message": "Component not found"}, 404

        return [option.to_dict() for option in component.options], 200

    def post(self, component_id):
        component = FormComponent.query.get(component_id)
        if not component:
            return {"message": "Component not found"}, 404

        data = request.get_json()
        option = ComponentOption(option=data['option'])
        component.options.append(option)

        db.session.commit()
        return option.to_dict(), 201

    def delete(self, component_id, option_id):
        option = ComponentOption.query.get(option_id)
        if not option or option.component_id != component_id:
            return {"message": "Option not found"}, 404
        db.session.delete(option)
        db.session.commit()
        return {"message": "Option deleted"}, 200


api.add_resource(FormResource, '/forms', '/forms/<int:form_id>')
api.add_resource(FormComponentResource, '/forms/<int:form_id>/components', '/forms/<int:form_id>/components/<int:component_id>')
api.add_resource(ComponentOptionResource, '/components/<int:component_id>/options', '/components/<int:component_id>/options/<int:option_id>')
