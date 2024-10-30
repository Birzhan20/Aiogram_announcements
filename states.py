from aiogram.fsm.state import StatesGroup, State


class CreateListing(StatesGroup):
    model = State()
    condition = State()
    price = State()
    description = State()
    photos = State()


class EditListing(StatesGroup):
    edit_listing_id = State()
    edit_listing_price = State()
    edit_listing_description = State()


class DeleteListing(StatesGroup):
    delete_listing_id = State()


class ToggleListing(StatesGroup):
    toggle_listing_id = State()


class SearchListing(StatesGroup):
    price_min = State()
    price_max = State()
    sorting = State()

