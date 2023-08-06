def get_api(load_info):
    from .app.Assembly  import Assembly

    Assembly.Assemble(load_info)
    return Assembly.api 

