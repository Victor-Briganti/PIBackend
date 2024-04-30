from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

# Salva o modelo de usuário atual em uma váriavel.
# Definido em "AUTH_USER_MODEL"
UserModel = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            firstname=validated_data["firstname"],
            lastname=validated_data["lastname"],
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                msg = "Não foi possível autenticar com as credenciais fornecidas."
                raise serializers.ValidationError(msg, code="authentication")

        else:
            msg = "É necessário fornecer um email e uma senha."
            raise serializers.ValidationError(msg, code="authentication")

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = "__all__"
        # read_only_fields = ("email",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def update(self, instance, validated_data):
        if "password" in validated_data:
            # Atualiza a senha com criptografia na instância e remove a mesma dos
            # dados validados.
            instance.set_password(validated_data.pop("password"))

        return super().update(instance, validated_data)
