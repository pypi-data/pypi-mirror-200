from rest_framework import serializers, viewsets
from rest_framework_yaml.parsers import YAMLParser
from rest_framework_yaml.renderers import YAMLRenderer
from .models import Application, Federation
from djangoldp_component.models import Component, Package


def format(value):
    match value.lower():
        case "false":
            return False
        case "true":
            return True
        case _:
            return value


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ("slug", "deploy")


class ApplicationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Application
        fields = ("slug", "deploy")


class ApplicationDetailSerializer(serializers.HyperlinkedModelSerializer):
    def to_representation(self, obj):
        application = super().to_representation(obj)

        federation = []
        for host in application["federation"]:
            federation.append(Federation.objects.get(urlid=host).target.api_url)

        serialized = {"apps": {"hosts": {}}}
        serialized["apps"]["hosts"][application["slug"]] = {
            "graphics": {
                "client": application["client_url"],
                "title": application["application_title"],
                "canva": application["repository"],
                "logo": application["application_logo"],
            },
            "data": {"api": application["api_url"], "with": federation},
            "packages": [],
            "components": [],
        }

        for applicationComponent in application["components"]:
            component = Component.objects.get(id=applicationComponent.obj.component_id)
            insertComponent = {
                "type": component.name,
                "route": False,
                "parameters": [],
                "extensions": [],
            }
            keys = []
            for parameter in applicationComponent.obj.parameters.all():
                if parameter.key == "route":
                    insertComponent["route"] = format(parameter.value)
                else:
                    i = {}
                    i[parameter.key] = format(parameter.value)
                    insertComponent["parameters"].append(i)
                keys.append(parameter.key)
            for parameter in component.parameters.all():
                if not parameter.key in keys:
                    if parameter.key == "route":
                        insertComponent["route"] = format(parameter.default)
                    else:
                        i = {}
                        i[parameter.key] = format(parameter.default)
                        insertComponent["parameters"].append(i)
            for extensionComponent in applicationComponent.obj.extensions.all():
                extension = Component.objects.get(id=extensionComponent.component_id)
                componentExtension = {
                    "type": extension.name,
                    "route": False,
                    "parameters": [],
                }
                keys = []
                for parameter in extensionComponent.parameters.all():
                    if parameter.key == "route":
                        componentExtension["route"] = format(parameter.value)
                    else:
                        i = {}
                        i[parameter.key] = format(parameter.value)
                        componentExtension["parameters"].append(i)
                    keys.append(parameter.key)
                for parameter in extension.parameters.all():
                    if not parameter.key in keys:
                        if parameter.key == "route":
                            componentExtension["route"] = format(parameter.default)
                        else:
                            i = {}
                            i[parameter.key] = format(parameter.default)
                            componentExtension["parameters"].append(i)
                insertComponent["extensions"].append(componentExtension)
            serialized["apps"]["hosts"][application["slug"]]["components"].append(
                insertComponent
            )

        insertDependencies = []
        for applicationPackage in application["packages"]:
            package = Package.objects.get(id=applicationPackage.obj.package_id)
            insertDependency = {
                "distribution": package.distribution,
                "module": package.module,
                "parameters": [],
            }
            keys = []
            for parameter in applicationPackage.obj.parameters.all():
                if not parameter.key in keys:
                    i = {}
                    i[parameter.key] = format(parameter.value)
                    insertDependency["parameters"].append(i)
                    keys.append(parameter.key)
            for parameter in package.parameters.all():
                if not parameter.key in keys:
                    i = {}
                    i[parameter.key] = format(parameter.default)
                    insertDependency["parameters"].append(i)
            insertDependencies.append(insertDependency)
        serialized["apps"]["hosts"][application["slug"]][
            "packages"
        ] = insertDependencies

        return serialized

    class Meta:
        model = Application
        lookup_field = "slug"
        fields = [
            "urlid",
            "slug",
            "api_url",
            "client_url",
            "application_title",
            "application_logo",
            "components",
            "packages",
            "repository",
            "federation",
        ]
        extra_kwargs = {"url": {"lookup_field": "slug"}}


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)


class ApplicationDetailViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationDetailSerializer
    lookup_field = "slug"
    parser_classes = (YAMLParser,)
    renderer_classes = (YAMLRenderer,)
