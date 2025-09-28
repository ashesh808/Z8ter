from z8ter.builders.app_builder import AppBuilder

app_builder = AppBuilder()
app_builder.use_config(".env")
app_builder.use_templating()
app_builder.use_vite()
app_builder.use_errors()

if __name__ == "__main__":
    app = app_builder.build(debug=True)
