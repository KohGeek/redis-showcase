import datetime

from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem
from prompt_toolkit import prompt, PromptSession, print_formatted_text as print, HTML
from prompt_toolkit.validation import Validator
from redis_om import (
    Field,
    HashModel,
    Migrator
)
from typing import Optional


class Comments(HashModel):
    title: str = Field(index=True)
    body: str
    name: Optional[str] = "Anonymous"
    datetime: datetime.datetime


def is_number(text):
    return text.isdigit()


def get_comment(prompt_text):
    comments = retrieve_comment(False)

    validator = Validator.from_callable(
        is_number,
        error_message='This input contains non-numeric characters',
        move_cursor_to_end=True)

    if comments:
        no = int(prompt(prompt_text, validator=validator))
        return comments[no]
    else:
        return None
    

def menu():
    menu = CursesMenu("Main Menu")
    create = FunctionItem("Create a comment", create_comment)
    retrieve = FunctionItem("View all comments", retrieve_comment)
    update = FunctionItem("Update a comment", update_comment)
    delete = FunctionItem("Delete a comment", delete_comment)

    menu.items.append(create)
    menu.items.append(retrieve)
    menu.items.append(update)
    menu.items.append(delete)

    return menu


def create_comment():
    prompt_session = PromptSession()
    title = prompt_session.prompt("Title: ")
    body = prompt_session.prompt("Body: ")
    name = prompt_session.prompt("Name: ")
    time = datetime.datetime.now()

    comment = Comments(title=title, body=body, name=name, datetime=time)
    comment.save()

    Migrator().run()

    print("Comment created.")
    input(ENTER_CONTINUE)


def retrieve_comment(wait=True):
    comments = Comments.find().all()
    if comments:
        for i, comment in enumerate(comments):
            print(HTML(f"{i}. <b>{comment.title}</b> by <i>{comment.name}</i> on <u>{comment.datetime}</u>"))
            print(HTML("------------------------------"))
            print(HTML(f"{comment.body}\n"))
    else:
        print("No comments found.")

    if wait:
        input(ENTER_CONTINUE)
    
    return comments


def update_comment():
    comment = get_comment("Select a comment to update: ")

    if comment is not None:
        body = prompt("\nBody: ", default=comment.body)
        comment.body = body
        comment.save()

        print("Comment updated.")

    input(ENTER_CONTINUE)


def delete_comment():
    comment = get_comment("Select a comment to delete: ")

    if comment is not None:
        pk = comment.pk
        Comments.delete(pk)

        print("Comment deleted.")

    input(ENTER_CONTINUE)
    
   
def main():
    mainmenu = menu()
    mainmenu.show()


if __name__ == '__main__':
    ENTER_CONTINUE = "\nPress enter to continue..."

    Migrator().run()
    main()
    retrieve_comment()