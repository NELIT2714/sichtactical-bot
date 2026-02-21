from aiogram import Router
from project.handlers import start_router, contact_handler

main_router = Router()
main_router.include_routers(start_router, contact_handler)
