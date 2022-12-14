"""
Redis Comment Box Showcase

Showcase of Redis with Python client, as requested by UECS3203 Advanced Database Systems.
The showcase targets a simple comment box system with username and timestamp.
"""
import datetime
import os
from typing import Optional

from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem
from prompt_toolkit import prompt, print_formatted_text, HTML
from prompt_toolkit.validation import Validator
from redis_om import (
    Field,
    HashModel,
    Migrator
)


class Comments(HashModel):
    """
    Comments
    Defines the Comments model.
    """
    title: str = Field(index=True)
    body: str
    name: Optional[str] = "Anonymous"
    datetime: datetime.datetime


def is_number(text):
    """Returns True if text is a number."""
    return text.isdigit()


def not_null(text):
    """Returns True if text is not null."""
    return text != ""


def get_comment(prompt_text):
    """Prompts users for a number and returns a comment if valid."""
    comments = retrieve_comment(False)

    validator = Validator.from_callable(
        is_number,
        error_message='This input contains non-numeric characters',
        move_cursor_to_end=True)

    num = int(prompt(prompt_text, validator=validator))

    try:
        return comments[num]
    except IndexError:
        print("Invalid selection.")
        return None


def get_input(prompt_text, optional=False):
    """Prompts users for a string and returns a string."""
    validator = None if optional else Validator.from_callable(
        not_null,
        error_message='This input is empty',
        move_cursor_to_end=True)

    return prompt(prompt_text, validator=validator)


def menu():
    """Main menu."""
    mainmenu = CursesMenu("Main Menu")
    create = FunctionItem("Create a comment", create_comment)
    retrieve = FunctionItem("View all comments", retrieve_comment)
    update = FunctionItem("Update a comment", update_comment)
    delete = FunctionItem("Delete a comment", delete_comment)

    mainmenu.items.append(create)
    mainmenu.items.append(retrieve)
    mainmenu.items.append(update)
    mainmenu.items.append(delete)

    return mainmenu


def create_comment():
    """Creates a comment."""
    title = get_input("Title: ")
    body = get_input("Body: ")
    name = get_input("Name: ", True)
    time = datetime.datetime.now()

    if not_null(name):
        comment = Comments(title=title, body=body, name=name, datetime=time)
    else:
        comment = Comments(title=title, body=body, datetime=time)

    comment.save()
    Migrator().run()

    print("Comment created.")
    input(ENTER_CONTINUE)


def retrieve_comment(wait=True):
    """Retrieves all comments."""
    os.system('cls' if os.name == 'nt' else 'clear')
    comments = Comments.find().all()
    if comments:
        for i, comment in enumerate(comments):
            print_formatted_text(HTML(
                f"{i}. <b>{comment.title}</b> by <i>{comment.name}"
                f"</i> on <u>{comment.datetime}</u>"))
            print_formatted_text(HTML("------------------------------"))
            print_formatted_text(HTML(f"{comment.body}\n"))
    else:
        print("No comments found.")

    if wait:
        input(ENTER_CONTINUE)

    return comments


def update_comment():
    """Updates a comment."""
    comment = get_comment("Select a comment to update: ")

    if comment is not None:
        body = prompt("\nBody: ", default=comment.body)
        comment.body = body
        comment.save()

        print("Comment updated.")

    input(ENTER_CONTINUE)


def delete_comment():
    """Deletes a comment."""
    comment = get_comment("Select a comment to delete: ")

    if comment is not None:
        primary_key = comment.pk
        Comments.delete(primary_key)

        print("Comment deleted.")

    input(ENTER_CONTINUE)


def main():
    """Main function. Displays main menu and migrates indexes."""
    Migrator().run()

    mainmenu = menu()
    mainmenu.show()


if __name__ == '__main__':
    ENTER_CONTINUE = "\nPress enter to continue..."
    main()
