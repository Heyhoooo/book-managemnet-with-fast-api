from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

books = {
    1 : {'title': 'Outlines of Dairy Technology', 'author' : 'Sukumar De', 'publish_year': 2002},
    2 : {'title': 'What technology wants', 'author' : 'Kevin Kelly', 'publish_year': 2010} ,
    3 : {'title': 'Technology in action', 'author' : 'Alan Evans', 'publish_year': 2004},
    4 : {'title': 'Ethics and technology', 'author' : 'Herman T. Tavani', 'publish_year': 2003},
}


@app.get('/books')
def get_books():
    for book in books:

        return book



class AddBook(BaseModel):
    title : str
    author : str
    publish_year : int


@app.post('/books')
def post_books(book : AddBook):
    new_book_id = max(books) + 1
    # book = AddBook()
    # books[id] = {'title': title, 'author': author, 'publish_year': publish_year}
    new_book = book.model_dump()
    books[new_book_id] = new_book

    return book


@app.get('/books/{id}')
def get_book_with_id(id : int):
    book = books.get(id)

    if book is None:
        raise HTTPException(
            status_code = 404,
            detail = 'book not found'
        )

    return book



class UpdateBook(BaseModel):
    title : str  | None = None
    author : str | None = None
    publish_year : int | None = None


@app.patch('/books/{id}')
def change_book_info(id : int, new_data : UpdateBook):
    book = books.get(id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail='book not found'
            )

    updated_book = new_data.model_dump(exclude_unset=True)

    if any(value is None for value in updated_book.values()):
        raise HTTPException(
            status_code=422,
            detail= 'fields shouldn\'t be null'
        )

    book.update(updated_book)

    return updated_book


@app.delete('/books/{id}')
def ommit_book(id:int):
    book = books.get(id)

    if book is None:
        raise HTTPException(
            status_code=404,
            detail= 'book not found'
        )
    removed = book
    books.pop(id)

    return f'book {removed} was deleted successfully!'