from flask import Blueprint


def create_blueprint_from_app_common(app):
    """Create  blueprint."""
    blueprint = app.extensions["common"].resource.as_blueprint()
    blueprint.record_once(init_create_blueprint_from_app_common)

    # calls record_once for all other functions starting with "init_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_addons_common") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint


def init_create_blueprint_from_app_common(state):
    """Init app."""
    app = state.app
    ext = app.extensions["common"]

    # register service
    sregistry = app.extensions["invenio-records-resources"].registry
    sregistry.register(ext.service, service_id="common")

    # Register indexer
    if hasattr(ext.service, "indexer"):
        iregistry = app.extensions["invenio-indexer"].registry
        iregistry.register(ext.service.indexer, indexer_id="common")


def create_blueprint_from_app_commonExt(app):
    """Create -ext blueprint."""
    blueprint = Blueprint("common-ext", __name__, url_prefix="common")
    blueprint.record_once(init_create_blueprint_from_app_common)

    # calls record_once for all other functions starting with "init_app_addons_"
    # https://stackoverflow.com/questions/58785162/how-can-i-call-function-with-string-value-that-equals-to-function-name
    funcs = globals()
    funcs = [
        v
        for k, v in funcs.items()
        if k.startswith("init_app_addons_common") and callable(v)
    ]
    for func in funcs:
        blueprint.record_once(func)

    return blueprint
