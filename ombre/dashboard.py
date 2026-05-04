
        if result["status"] == "completed":
            validator.validate_batch(result.get("trace_ids",[]))

        return jsonify(result)

    # ── Billing endpoints ───────────────────────────────────────────────────

    @app.route("/api/billing/summary")
    def api_billing_summary():
        client_id = request.args.get("client_id","demo_client")
        billing   = get_billing_engine()
        client    = billing.get_client(client_id)
        if not client:
            return jsonify({"error": "Client not found. Register first."}), 404
        summary = billing.get_billing_summary(client_id)
        return jsonify(summary.to_dict())

    @app.route("/api/billing/payment-page")
    def api_payment_page():
        client_id = request.args.get("client_id","demo_client")
        billing   = get_billing_engine()
        return jsonify(billing.get_payment_page_data(client_id))

    @app.route("/api/billing/payment-sent", methods=["POST"])
    def api_payment_sent():
        data = request.get_json(silent=True) or {}
        billing = get_billing_engine()
        result  = billing.record_payment_intent(
            client_id=data.get("client_id", "demo_client"),
            amount=float(data.get("amount", 0)),
            statement_id=data.get("statement_id", "")
        )
        return jsonify(result)

    @app.route("/api/billing/history")
    def api_billing_history():
        client_id = request.args.get("client_id","demo_client")
        days      = int(request.args.get("days", 30))
        billing   = get_billing_engine()
        return jsonify(billing.get_usage_history(client_id, days))

    @app.route("/api/billing/platform")
    def api_platform_revenue():
        billing = get_billing_engine()
        return jsonify(billing.platform_revenue_summary())

    # ── Client registration ─────────────────────────────────────────────────

    @app.route("/api/clients/register", methods=["POST"])
    def api_register_client():
        data    = request.get_json(silent=True) or {}
        billing = get_billing_engine()
        result  = billing.register_client(
            name=data.get("name",""),
            email=data.get("email",""),
            monthly_minimum=float(data.get("monthly_minimum",5000))
        )
        return jsonify(result)

    # ── Analytics endpoints ─────────────────────────────────────────────────

    @app.route("/api/analytics/platform")
    def api_platform_analytics():
        analytics = get_analytics()
        return jsonify(analytics.get_platform_analytics())

    @app.route("/api/analytics/client")
    def api_client_analytics():
        client_id = request.args.get("client_id","demo_client")
        analytics = get_analytics()
        return jsonify(analytics.get_client_analytics(client_id))

    @app.route("/api/analytics/heatmap")
    def api_heatmap():
        analytics = get_analytics()
        return jsonify(analytics.get_demand_heatmap())

    # ── RAG endpoints ──────────────────────────────────────────────────────

    @app.route("/api/rag/search")
    def api_rag_search():
        from ombre.rag import get_rag_engine
        from ombre.billing.engine import get_billing_engine
        from ombre.trust import enrich_traces
        client_id = request.args.get("client_id", "demo_client")
        query = request.args.get("q", "")
        if not query:
            return jsonify({"error": "q parameter required"}), 400
        rag = get_rag_engine()
        billing = get_billing_engine()
        results = rag.search(
            query=query,
            top_k=int(request.args.get("top_k", 10)),
            domain=request.args.get("domain"),
            min_score=float(request.args.get("min_score", 85)),
            quality_tier=request.args.get("quality_tier"),
            min_similarity=float(request.args.get("min_similarity", 0.0)),
        )
        total = 0.0
        for t in results:
            log = billing.meter_call(client_id=client_id, call_type="trace_retrieval",
                trace_id=t.get("trace_id"), is_premium=t.get("quality_tier")=="premium",
                metadata={"rag_query": query[:100]})
            total += log.amount_charged
        return jsonify({"query": query, "results": enrich_traces(results),
                        "count": len(results), "total_charged": round(total, 4),
                        "retrieval_type": "semantic_rag"})

    @app.route("/api/rag/similar/<trace_id>")
    def api_rag_similar(trace_id):
        from ombre.rag import get_rag_engine
        rag = get_rag_engine()
        results = rag.get_similar_traces(trace_id, top_k=int(request.args.get("top_k", 5)))
        return jsonify({"reference": trace_id, "similar": results, "count": len(results)})

    @app.route("/api/rag/stats")
    def api_rag_stats():
        from ombre.rag import get_rag_engine
        return jsonify(get_rag_engine().get_index_stats())

    @app.route("/api/rag/build", methods=["POST"])
    def api_rag_build():
        from ombre.rag import get_rag_engine
        rag = get_rag_engine()
        result = rag.build_index(force=True)
        return jsonify(result)

    # ── Trust & Safety endpoints ───────────────────────────────────────────

    @app.route("/v1/trust/audit/<trace_id>")
    def api_trust_audit(trace_id):
        from ombre.trust import get_trust_engine
        trust = get_trust_engine()
        result = trust.get_audit_trail(trace_id)
        if not result:
            return jsonify({"error": f"Trace {trace_id} not found"}), 404
        return jsonify(result)

    @app.route("/v1/trust/data-card")
    def api_trust_data_card():
        from ombre.trust import get_trust_engine
        return jsonify(get_trust_engine().get_data_card())

    @app.route("/v1/trust/model-card")
    def api_trust_model_card():
        from ombre.trust import get_trust_engine
        return jsonify(get_trust_engine().get_model_card())

    @app.route("/v1/trust/security")
    def api_trust_security():
        from ombre.trust import get_trust_engine
        return jsonify(get_trust_engine().get_security())

    @app.route("/v1/trust/stats")
    def api_trust_stats():
        from ombre.trust import get_trust_engine
        return jsonify(get_trust_engine().get_live_stats())

    # ── Health check ───────────────────────────────────────────────────────

    @app.route("/api/health")
    def api_health():
        return jsonify({
            "status": "ok",
            "version": "1.0.0",
            "service": "ombre-reasoning-data-infrastructure",
            "trust_endpoints": [
                "/v1/trust/audit/{trace_id}",
                "/v1/trust/data-card",
                "/v1/trust/model-card",
                "/v1/trust/security",
                "/v1/trust/stats",
            ]
        })

    return app


def run_dashboard(port: int = 8080, host: str = "0.0.0.0"):
    """Run the dashboard server."""
    app = create_app()
    import logging
    log = logging.getLogger("werkzeug")
    log.setLevel(logging.ERROR)
    print(f"[Dashboard] Ombre dashboard running at http://localhost:{port}")
    app.run(host=host, port=port, debug=False, threaded=True)
