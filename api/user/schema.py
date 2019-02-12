import graphene

from graphene_sqlalchemy import (SQLAlchemyObjectType)
# from graphql import GraphQLError
from api.user.models import User as UserModel
from helpers.authentication.auth import register


class User(SQLAlchemyObjectType):

    class Meta:
        model = UserModel


class RegisterUser(graphene.Mutation):

    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
    user = graphene.Field(User)

    def mutate(self, info, **kwargs):
        print("the kwargs are>>>>>>>>>>>", kwargs)
        user = UserModel(**kwargs)
        register(**kwargs)
        # with SaveContextManager(user, kwargs.get('email'), 'User email'):     
        return RegisterUser(user=user)


class Query(graphene.ObjectType):
    user = graphene.List(User)

    # def resolve_users(self, info, **kwargs):
    #     response = PaginatedUsers(**kwargs)
    #     return response

    def resolve_user(self, info):
        query = User.get_query(info)
        print("the query is ", query)
        return query.all()


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    # create_user = CreateUser.Field()
    # delete_user = DeleteUser.Field()
    # change_user_role = ChangeUserRole.Field()
