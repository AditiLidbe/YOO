# from fastapi import Depends,HTTPException,status
# from ..jwt.handler import get_current_user
# from ...Authentication_Flow.authentication_schema.auth_schema import TokenData
# from ...Authentication_Flow.authentication_model.role_model import Role


# allowed_roles={role.value for role in Role}

# def role_necessary(allowed_roles: list[str]):
#     def only_role(user:TokenData=Depends(get_current_user)):
#         user_roles = [role for role in (user.roles or [])]
#         allowed=False
#         for user_role in user_roles:
#             for allowed_role in allowed_roles:
#                 if user_role ==allowed_role:
#                     allowed=True
#         if allowed==False:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Insufficient permissions."
#             )
#         return user
#     return only_role



# # 


