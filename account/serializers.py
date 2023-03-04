from rest_framework import serializers
from .models import User

class UserregisterSerializer(serializers.ModelSerializer):

    password2=serializers.CharField(style={'input_type':'password'},
                                    write_only=True)
    
    class Meta:
        model=User
        fields=['email','name','password','password2','tc']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password!=password2:
            raise serializers.ValidationError("password did not matched")
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)



class UserLoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=User
        exclude=['name','tc']

class UserprofileSerializer(serializers.ModelSerializer):

    class Meta:
        model=User
        fields=['id','email','name','password','tc']


class UserPasswordChangeSerializer(serializers.ModelSerializer):
    password=serializers.CharField(style={'input_type':'password'},
                                    write_only=True)
    password2=serializers.CharField(style={'input_type':'password'},
                                    write_only=True)

    class Meta:
        model=User
        fields=['password','password2']
        

    def validate(self, attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password!=password2:
            raise serializers.ValidationError("password did not matched")
        
        user.set_password(password)
        user.save()

        return attrs