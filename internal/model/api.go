package model

import "encoding/json"

func (r *Response[T]) ToJSON() ([]byte, error) {
	return json.Marshal(r)
}
