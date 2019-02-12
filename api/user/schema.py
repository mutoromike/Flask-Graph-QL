import graphene

from graphene_sqlalchemy import (SQLAlchemyObjectType)
from graphql import GraphQLError
from api.user.models import User as UserModel
# from api.user_role.models import UsersRole
# from helpers.auth.user_details import get_user_from_db
from helpers.authentication.auth import register
# from helpers.auth.validator import verify_email
# from helpers.pagination.paginate import Paginate, validate_page
# from helpers.auth.error_handler import SaveContextManager


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
        #     
        return RegisterUser(user=user)

# class CreateUser(graphene.Mutation):

#     class Arguments:
#         email = graphene.String(required=True)
#         name = graphene.String(required=True)
#         password = graphene.String(required=True)
#     user = graphene.Field(User)

#     def mutate(self, info, **kwargs):
#         user = UserModel(**kwargs)
#         with SaveContextManager(user, kwargs.get('email'), 'User email'):
#             return CreateUser(user=user)


class Query(graphene.ObjectType):
    # users = graphene.Field(PaginatedUsers, page=graphene.Int(),
    #                        per_page=graphene.Int())
    user = graphene.List(User)

    # def resolve_users(self, info, **kwargs):
    #     response = PaginatedUsers(**kwargs)
    #     return response

    def resolve_user(self, info):
        query = User.get_query(info)
        print("the query is ", query)
        return query.all()


# class DeleteUser(graphene.Mutation):
#     class Arguments:
#         email = graphene.String(required=True)
#     user = graphene.Field(User)

#     @Auth.user_roles('Admin')
#     def mutate(self, info, email, **kwargs):
#         query_user = User.get_query(info)
#         exact_query_user = query_user.filter(
#             UserModel.email == email).first()
#         user_from_db = get_user_from_db()
#         if not verify_email(email):
#             raise GraphQLError("Invalid email format")
#         if not exact_query_user:
#             raise GraphQLError("User not found")
#         if user_from_db.email == email:
#             raise GraphQLError("You cannot delete yourself")
#         exact_query_user.delete()
#         return DeleteUser(user=exact_query_user)


# class ChangeUserRole(graphene.Mutation):
#     class Arguments:

#         email = graphene.String(required=True)
#         role_id = graphene.Int()
#     user = graphene.Field(User)

#     @Auth.user_roles('Admin')
#     def mutate(self, info, email, **kwargs):
#         query_user = User.get_query(info)
#         exact_user = query_user.filter(
#             UserModel.email == email).first()
#         if not exact_user:
#             raise GraphQLError("User not found")
#         user_role = UsersRole.query.filter_by(user_id=exact_user.id).first()
#         new_role = kwargs.pop('role_id')
#         user_role.role_id = new_role
#         user_role.save()
#         return ChangeUserRole(user=exact_user)


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    # create_user = CreateUser.Field()
    # delete_user = DeleteUser.Field()
    # change_user_role = ChangeUserRole.Field()
