from fasthtml.common import *
import uvicorn

db = database('data/todos_qa.db')
todos = db.t.todos
if todos not in db.t: todos.create(id=int, QAtype=str, QAcontent=str, done=bool, pk='id')
Todo = todos.dataclass()

app = FastHTML(hdrs=[picolink])
rt = app.route

@patch
def __ft__(self:Todo):
   done = "✅" if self.done else ""
   link = AX(self.QAtype, hx_get=f'/QAconv/{self.id}', target_id='details')
   edit = AX('edit', hx_get=f'/edit/{self.id}', target_id='details')
   return Li(done, link, ' | ', edit, id=f'QAconv-{self.id}')

#def get_newinp(): return Input(placeholder="Type", name="QAtype", hx_swap_oob="true", id="QAtype")
def get_newinp(): return Select(Option("Question"), Option("Goal_B"), name="QAtype", hx_swap_oob="true", id="QAtype")
def get_newinp2(): return Input(placeholder="Content", name="QAcontent", hx_swap_oob="true", id="QAcontent")
def get_footer(): return Div(hx_swap_oob='true', id="details")

# ---
#    return Titled('HTMX Form Demo', Grid(
#        Form(hx_post="/submit", hx_target="#result", hx_trigger="input delay:200ms")(
#            Select(Option("One"), Option("Two"), id="select"),
#            Input(value='j', type="text", id="name", placeholder="Name"),
#            Input(value='h', type="text", id="email", placeholder="Email")),
#        Div(id="result")
#    ))

# ---
@rt("/")
def get():
  todolist = Ul(*todos(), id="todolist")
  header = Form(Group(get_newinp(), get_newinp2(), Button("Add")),
                hx_post="/", target_id="todolist", hx_swap="beforeend")
  card = Card(todolist, header=header, footer=get_footer())
  contents = Main(H1("QA conversation"), card, cls="container")
  return Title("QA conversation"), contents

@rt("/")
def post(todo:Todo): return todos.insert(todo), get_newinp(), get_newinp2()

@rt("/QAconv/{id}")
def delete(id:int):
   todos.delete(id)
   return get_footer()

@rt("/QAconv/{id}")
def get(id:int):
  todo = todos[id]
  btn = Button('Delete', hx_delete=f'/QAconv/{id}', target_id=f'QAconv-{id}', hx_swap="delete")
  return P(todo.QAtype), P(todo.QAcontent), btn

@rt("/edit/{id}")
def get(id:int):
    res = Form(Group(Input(id="QAtype"), Input(id="QAcontent"), Button("Save")),
        Hidden(id="id"), CheckboxX(id="done", label='Done'),
        hx_put="/", target_id=f'QAconv-{id}', id="edit")
    return fill_form(res, todos.get(id))

@rt("/")
def put(todo: Todo): return todos.update(todo), get_footer()

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.getenv("PORT", default=8000)))
