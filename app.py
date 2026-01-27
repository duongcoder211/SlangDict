from fastapi import FastAPI, Request, Response
from endpoints.routes import routes, lifespan
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates

app = FastAPI(lifespan=lifespan)
app.include_router(router=routes)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: StarletteHTTPException):
    # Dont need  param 'response' as input. 
    # TemplateResponse will create a Response with specify status_code.

    return templates.TemplateResponse(
        name="404_page.html",
        context={"request": request}, # Have to request in context for Jinja2
        status_code=404 
    )

# Params
# debug: bool = False,
# routes: list[BaseRoute] | None = None,
# title: str = "FastAPI",
# summary: str | None = None,
# description: str = "",
# version: str = "0.1.0",
# openapi_url: str | None = "/openapi.json",
# openapi_tags: list[dict[str,Any]] | None = None,
# servers: list[dict[str,str | Any]] | None = None,
# dependencies: Sequence[Depends] | None = None,
# default_response_class: type[Response] = Default(JSONResponse),
# redirect_slashes: bool = True,
# docs_url: str | None = "/docs",
# redoc_url: str | None = "/redoc",
# swagger_ui_oauth2_redirect_url: str | None = "/docs/oauth2-redirect",
# swagger_ui_init_oauth: dict[str,Any] | None = None,
# middleware: Sequence[Middleware] | None = None,
# exception_handlers: dict[int | type[Exception],(Request,Any) -> Coroutine[Any,Any,Response]] | None = None,
# on_startup: Sequence[() -> Any] | None = None,
# on_shutdown: Sequence[() -> Any] | None = None,
# lifespan: StatelessLifespan[FastAPI] | StatefulLifespan[FastAPI] | None = None,
# terms_of_service: str | None = None,
# contact: dict[str,str | Any] | None = None,
# license_info: dict[str,str | Any] | None = None,
# openapi_prefix: str = "",
# root_path: str = "",
# root_path_in_servers: bool = True,
# responses: dict[int | str,dict[str,Any]] | None = None,
# callbacks: list[BaseRoute] | None = None,
# webhooks: APIRouter | None = None,
# deprecated: bool | None = None,
# include_in_schema: bool = True,
# swagger_ui_parameters: dict[str,Any] | None = None,
# generate_unique_id_function: (APIRoute) -> str = Default(generate_unique_id),
# separate_input_output_schemas: bool = True,
# openapi_external_docs: dict[str,Any] | None = None,
