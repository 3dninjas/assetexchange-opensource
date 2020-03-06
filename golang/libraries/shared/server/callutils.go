package server

import "reflect"

func isChannelType(t reflect.Type, dir reflect.ChanDir) bool {
	return t.Kind() == reflect.Chan && t.ChanDir() == dir
}

func isErrorType(t reflect.Type) bool {
	return t == reflect.TypeOf((*error)(nil)).Elem()
}

func isErrorChannelType(t reflect.Type, dir reflect.ChanDir) bool {
	return t.Kind() == reflect.Chan && isErrorType(t.Elem()) && t.ChanDir() == dir
}
