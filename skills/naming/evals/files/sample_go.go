package handlers

import (
	"context"
	"encoding/json"
	"net/http"
)

type UMgr struct {
	db  DBConn
	cfg *Cfg
}

func (m *UMgr) Proc(ctx context.Context, w http.ResponseWriter, r *http.Request) {
	var d map[string]interface{}
	json.NewDecoder(r.Body).Decode(&d)

	n := d["n"].(string)
	e := d["e"].(string)
	active := true

	u, err := m.db.GetByEmail(ctx, e)
	if err != nil {
		http.Error(w, "bad", 500)
		return
	}

	if u != nil {
		http.Error(w, "exists", 409)
		return
	}

	nu := &User{Name: n, Email: e, Active: active}
	m.db.Save(ctx, nu)
	json.NewEncoder(w).Encode(nu)
}
