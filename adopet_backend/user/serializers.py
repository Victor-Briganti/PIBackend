from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import Address, Adopter

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


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "zip_code",
            "street",
            "number",
            "complement",
            "city",
            "state",
            "district",
        ]


class AdopterSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Adopter
        fields = ["cpf", "phone", "birth_date", "address"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        # Cria um adotante e um endereço associado.
        address_data = validated_data.pop("address")
        address = Address.objects.create(**address_data)
        adopter = Adopter.objects.create(address=address, **validated_data)
        return adopter

    def update(self, instance, validated_data):
        # Se existir um endereço associado ao adotante, atualiza o mesmo.
        address_data = validated_data.pop("address", None)
        if address_data:
            address = instance.address
            address.zip_code = address_data.get("zip_code", address.zip_code)
            address.street = address_data.get("street", address.street)
            address.number = address_data.get("number", address.number)
            address.complement = address_data.get("complement", address.complement)
            address.city = address_data.get("city", address.city)
            address.state = address_data.get("state", address.state)
            address.district = address_data.get("district", address.district)
            address.save()
        instance.cpf = validated_data.get("cpf", instance.cpf)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        instance.save()
        return super().update(instance, validated_data)

    def destroy(self, instance):
        instance.address.delete()
        instance.delete()
        return instance


class UserSerializer(serializers.ModelSerializer):
    adopter = AdopterSerializer(required=False)

    class Meta:
        model = UserModel
        fields = "__all__"
        read_only_fields = ("email",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def update(self, instance, validated_data):
        if "password" in validated_data:
            # Atualiza a senha com criptografia na instância e remove a mesma dos
            # dados validados.
            instance.set_password(validated_data.pop("password"))

        return super().update(instance, validated_data)


class AdopterListSerializer(serializers.ModelSerializer):
    # Definido campos de endereço associados ao adotante.
    address_id = serializers.IntegerField(source="address.id", read_only=True)
    street = serializers.CharField(source="address.street", read_only=True)
    city = serializers.CharField(source="address.city", read_only=True)
    state = serializers.CharField(source="address.state", read_only=True)
    zip_code = serializers.CharField(source="address.zip_code", read_only=True)
    number = serializers.CharField(source="address.number", read_only=True)
    complement = serializers.CharField(source="address.complement", read_only=True)
    district = serializers.CharField(source="address.district", read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Adopter
        fields = [
            "id",
            "birth_date",
            "phone",
            "cpf",
            "user_id",
            "address_id",
            "street",
            "city",
            "state",
            "zip_code",
            "number",
            "complement",
            "district",
            "is_active",
        ]
        read_only_fields = ["id"]
