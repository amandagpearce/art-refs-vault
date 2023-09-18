    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        tokenExists = TokenBlocklistModel.query.filter(
            TokenBlocklistModel.token == jwt_payload["jti"]
        ).first()

        return tokenExists

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "Token não é do tipo fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "Token revogado.", "error": "token_revoked"}
            ),
            401,
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(
            {
                "message": "Token expirado.",
                "error": "invalid_token",
            },
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify(
            {
                "message": "Assinatura de verificação falhou.",
                "error": "invalid_token",
            },
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify(
            {
                "description": "Request não contém token de acesso",
                "error": "authorization_required",
            },
            401,
        )
