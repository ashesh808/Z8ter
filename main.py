from z8ter.builders.app_builder import AppBuilder
from app.identity.data.session_repo import InMemorySessionRepo
from app.identity.data.user_repo import InMemoryUserRepo

app_builder = AppBuilder()
app_builder.use_config(".env")
app_builder.use_templating()
app_builder.use_vite()
app_builder.use_auth_repos(
    session_repo=InMemorySessionRepo(),
    user_repo=InMemoryUserRepo()
)
app_builder.use_authentication()
app_builder.use_errors()

if __name__ == "__main__":
    app = app_builder.build()
