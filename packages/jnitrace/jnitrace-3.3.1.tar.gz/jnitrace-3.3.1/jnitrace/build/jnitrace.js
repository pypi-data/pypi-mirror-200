(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
});

const t = require("jnitrace-engine"), e = require("jnitrace-engine"), a = require("jnitrace-engine"), r = require("jnitrace-engine"), c = require("./utils/method_data"), o = require("./transport/data_transport"), I = !1, n = new o.DataTransport;

let l = null;

t.JNILibraryWatcher.setCallback({
  onLoaded(t) {
    if (!a.Config.initialised()) {
      recv("config", (t => {
        const e = new r.ConfigBuilder;
        e.libraries = t.payload.libraries, e.backtrace = t.payload.backtrace, e.includeExports = t.payload.include_export, 
        e.excludeExports = t.payload.exclude_export, e.env = t.payload.env, e.vm = t.payload.vm, 
        l = e.build(), n.setIncludeFilter(t.payload.include), n.setExcludeFilter(t.payload.exclude);
      })).wait();
    }
    null !== l && l.libraries.forEach((e => {
      t.includes(e) && send({
        type: "tracked_library",
        library: t
      });
    }));
  }
});

const h = {
  onEnter(t) {
    this.args = t;
  },
  onLeave(t) {
    const e = new c.MethodData(this.methodDef, this.args, t.get(), this.javaMethod);
    n.reportJNIEnvCall(e, this.backtrace);
  }
}, N = {
  onEnter(t) {
    this.args = t;
  },
  onLeave(t) {
    const e = new c.MethodData(this.methodDef, this.args, t.get(), this.javaMethod);
    n.reportJavaVMCall(e, this.backtrace);
  }
};

e.JNIInterceptor.attach("DestroyJavaVM", N), e.JNIInterceptor.attach("AttachCurrentThread", N), 
e.JNIInterceptor.attach("DetachCurrentThread", N), e.JNIInterceptor.attach("GetEnv", N), 
e.JNIInterceptor.attach("AttachCurrentThreadAsDaemon", N), e.JNIInterceptor.attach("GetVersion", h), 
e.JNIInterceptor.attach("DefineClass", h), e.JNIInterceptor.attach("FindClass", h), 
e.JNIInterceptor.attach("FromReflectedMethod", h), e.JNIInterceptor.attach("FromReflectedField", h), 
e.JNIInterceptor.attach("ToReflectedMethod", h), e.JNIInterceptor.attach("GetSuperclass", h), 
e.JNIInterceptor.attach("IsAssignableFrom", h), e.JNIInterceptor.attach("ToReflectedField", h), 
e.JNIInterceptor.attach("Throw", h), e.JNIInterceptor.attach("ThrowNew", h), e.JNIInterceptor.attach("ExceptionOccurred", h), 
e.JNIInterceptor.attach("ExceptionDescribe", h), e.JNIInterceptor.attach("ExceptionClear", h), 
e.JNIInterceptor.attach("FatalError", h), e.JNIInterceptor.attach("PushLocalFrame", h), 
e.JNIInterceptor.attach("PopLocalFrame", h), e.JNIInterceptor.attach("NewGlobalRef", h), 
e.JNIInterceptor.attach("DeleteGlobalRef", h), e.JNIInterceptor.attach("DeleteLocalRef", h), 
e.JNIInterceptor.attach("IsSameObject", h), e.JNIInterceptor.attach("NewLocalRef", h), 
e.JNIInterceptor.attach("EnsureLocalCapacity", h), e.JNIInterceptor.attach("AllocObject", h), 
e.JNIInterceptor.attach("NewObject", h), e.JNIInterceptor.attach("NewObjectV", h), 
e.JNIInterceptor.attach("NewObjectA", h), e.JNIInterceptor.attach("GetObjectClass", h), 
e.JNIInterceptor.attach("IsInstanceOf", h), e.JNIInterceptor.attach("GetMethodID", h), 
e.JNIInterceptor.attach("CallObjectMethod", h), e.JNIInterceptor.attach("CallObjectMethodV", h), 
e.JNIInterceptor.attach("CallObjectMethodA", h), e.JNIInterceptor.attach("CallBooleanMethod", h), 
e.JNIInterceptor.attach("CallBooleanMethodV", h), e.JNIInterceptor.attach("CallBooleanMethodA", h), 
e.JNIInterceptor.attach("CallByteMethod", h), e.JNIInterceptor.attach("CallByteMethodV", h), 
e.JNIInterceptor.attach("CallByteMethodA", h), e.JNIInterceptor.attach("CallCharMethod", h), 
e.JNIInterceptor.attach("CallCharMethodV", h), e.JNIInterceptor.attach("CallCharMethodA", h), 
e.JNIInterceptor.attach("CallShortMethod", h), e.JNIInterceptor.attach("CallShortMethodV", h), 
e.JNIInterceptor.attach("CallShortMethodA", h), e.JNIInterceptor.attach("CallIntMethod", h), 
e.JNIInterceptor.attach("CallIntMethodV", h), e.JNIInterceptor.attach("CallIntMethodA", h), 
e.JNIInterceptor.attach("CallLongMethod", h), e.JNIInterceptor.attach("CallLongMethodV", h), 
e.JNIInterceptor.attach("CallLongMethodA", h), e.JNIInterceptor.attach("CallFloatMethod", h), 
e.JNIInterceptor.attach("CallFloatMethodV", h), e.JNIInterceptor.attach("CallFloatMethodA", h), 
e.JNIInterceptor.attach("CallDoubleMethod", h), e.JNIInterceptor.attach("CallDoubleMethodV", h), 
e.JNIInterceptor.attach("CallDoubleMethodA", h), e.JNIInterceptor.attach("CallVoidMethod", h), 
e.JNIInterceptor.attach("CallVoidMethodV", h), e.JNIInterceptor.attach("CallVoidMethodA", h), 
e.JNIInterceptor.attach("CallNonvirtualObjectMethod", h), e.JNIInterceptor.attach("CallNonvirtualObjectMethodV", h), 
e.JNIInterceptor.attach("CallNonvirtualObjectMethodA", h), e.JNIInterceptor.attach("CallNonvirtualBooleanMethod", h), 
e.JNIInterceptor.attach("CallNonvirtualBooleanMethodV", h), e.JNIInterceptor.attach("CallNonvirtualBooleanMethodA", h), 
e.JNIInterceptor.attach("CallNonvirtualByteMethod", h), e.JNIInterceptor.attach("CallNonvirtualByteMethodV", h), 
e.JNIInterceptor.attach("CallNonvirtualByteMethodA", h), e.JNIInterceptor.attach("CallNonvirtualCharMethod", h), 
e.JNIInterceptor.attach("CallNonvirtualCharMethodV", h), e.JNIInterceptor.attach("CallNonvirtualCharMethodA", h), 
e.JNIInterceptor.attach("CallNonvirtualShortMethod", h), e.JNIInterceptor.attach("CallNonvirtualShortMethodV", h), 
e.JNIInterceptor.attach("CallNonvirtualShortMethodA", h), e.JNIInterceptor.attach("CallNonvirtualIntMethod", h), 
e.JNIInterceptor.attach("CallNonvirtualIntMethodV", h), e.JNIInterceptor.attach("CallNonvirtualIntMethodA", h), 
e.JNIInterceptor.attach("CallNonvirtualLongMethod", h), e.JNIInterceptor.attach("CallNonvirtualLongMethodV", h), 
e.JNIInterceptor.attach("CallNonvirtualLongMethodA", h), e.JNIInterceptor.attach("CallNonvirtualFloatMethod", h), 
e.JNIInterceptor.attach("CallNonvirtualFloatMethodV", h), e.JNIInterceptor.attach("CallNonvirtualFloatMethodA", h), 
e.JNIInterceptor.attach("CallNonvirtualDoubleMethod", h), e.JNIInterceptor.attach("CallNonvirtualDoubleMethodV", h), 
e.JNIInterceptor.attach("CallNonvirtualDoubleMethodA", h), e.JNIInterceptor.attach("CallNonvirtualVoidMethod", h), 
e.JNIInterceptor.attach("CallNonvirtualVoidMethodV", h), e.JNIInterceptor.attach("CallNonvirtualVoidMethodA", h), 
e.JNIInterceptor.attach("GetFieldID", h), e.JNIInterceptor.attach("GetObjectField", h), 
e.JNIInterceptor.attach("GetBooleanField", h), e.JNIInterceptor.attach("GetByteField", h), 
e.JNIInterceptor.attach("GetCharField", h), e.JNIInterceptor.attach("GetShortField", h), 
e.JNIInterceptor.attach("GetIntField", h), e.JNIInterceptor.attach("GetLongField", h), 
e.JNIInterceptor.attach("GetFloatField", h), e.JNIInterceptor.attach("GetDoubleField", h), 
e.JNIInterceptor.attach("SetObjectField", h), e.JNIInterceptor.attach("SetBooleanField", h), 
e.JNIInterceptor.attach("SetByteField", h), e.JNIInterceptor.attach("SetCharField", h), 
e.JNIInterceptor.attach("SetShortField", h), e.JNIInterceptor.attach("SetIntField", h), 
e.JNIInterceptor.attach("SetLongField", h), e.JNIInterceptor.attach("SetFloatField", h), 
e.JNIInterceptor.attach("SetDoubleField", h), e.JNIInterceptor.attach("GetStaticMethodID", h), 
e.JNIInterceptor.attach("CallStaticObjectMethod", h), e.JNIInterceptor.attach("CallStaticObjectMethodV", h), 
e.JNIInterceptor.attach("CallStaticObjectMethodA", h), e.JNIInterceptor.attach("CallStaticBooleanMethod", h), 
e.JNIInterceptor.attach("CallStaticBooleanMethodV", h), e.JNIInterceptor.attach("CallStaticBooleanMethodA", h), 
e.JNIInterceptor.attach("CallStaticByteMethod", h), e.JNIInterceptor.attach("CallStaticByteMethodV", h), 
e.JNIInterceptor.attach("CallStaticByteMethodA", h), e.JNIInterceptor.attach("CallStaticCharMethod", h), 
e.JNIInterceptor.attach("CallStaticCharMethodV", h), e.JNIInterceptor.attach("CallStaticCharMethodA", h), 
e.JNIInterceptor.attach("CallStaticShortMethod", h), e.JNIInterceptor.attach("CallStaticShortMethodV", h), 
e.JNIInterceptor.attach("CallStaticShortMethodA", h), e.JNIInterceptor.attach("CallStaticIntMethod", h), 
e.JNIInterceptor.attach("CallStaticIntMethodV", h), e.JNIInterceptor.attach("CallStaticIntMethodA", h), 
e.JNIInterceptor.attach("CallStaticLongMethod", h), e.JNIInterceptor.attach("CallStaticLongMethodV", h), 
e.JNIInterceptor.attach("CallStaticLongMethodA", h), e.JNIInterceptor.attach("CallStaticFloatMethod", h), 
e.JNIInterceptor.attach("CallStaticFloatMethodV", h), e.JNIInterceptor.attach("CallStaticFloatMethodA", h), 
e.JNIInterceptor.attach("CallStaticDoubleMethod", h), e.JNIInterceptor.attach("CallStaticDoubleMethodV", h), 
e.JNIInterceptor.attach("CallStaticDoubleMethodA", h), e.JNIInterceptor.attach("CallStaticVoidMethod", h), 
e.JNIInterceptor.attach("CallStaticVoidMethodV", h), e.JNIInterceptor.attach("CallStaticVoidMethodA", h), 
e.JNIInterceptor.attach("GetStaticFieldID", h), e.JNIInterceptor.attach("GetStaticObjectField", h), 
e.JNIInterceptor.attach("GetStaticBooleanField", h), e.JNIInterceptor.attach("GetStaticByteField", h), 
e.JNIInterceptor.attach("GetStaticCharField", h), e.JNIInterceptor.attach("GetStaticShortField", h), 
e.JNIInterceptor.attach("GetStaticIntField", h), e.JNIInterceptor.attach("GetStaticLongField", h), 
e.JNIInterceptor.attach("GetStaticFloatField", h), e.JNIInterceptor.attach("GetStaticDoubleField", h), 
e.JNIInterceptor.attach("SetStaticObjectField", h), e.JNIInterceptor.attach("SetStaticBooleanField", h), 
e.JNIInterceptor.attach("SetStaticByteField", h), e.JNIInterceptor.attach("SetStaticCharField", h), 
e.JNIInterceptor.attach("SetStaticShortField", h), e.JNIInterceptor.attach("SetStaticIntField", h), 
e.JNIInterceptor.attach("SetStaticLongField", h), e.JNIInterceptor.attach("SetStaticFloatField", h), 
e.JNIInterceptor.attach("SetStaticDoubleField", h), e.JNIInterceptor.attach("NewString", h), 
e.JNIInterceptor.attach("GetStringLength", h), e.JNIInterceptor.attach("GetStringChars", h), 
e.JNIInterceptor.attach("ReleaseStringChars", h), e.JNIInterceptor.attach("NewStringUTF", h), 
e.JNIInterceptor.attach("GetStringUTFLength", h), e.JNIInterceptor.attach("GetStringUTFChars", h), 
e.JNIInterceptor.attach("ReleaseStringUTFChars", h), e.JNIInterceptor.attach("GetArrayLength", h), 
e.JNIInterceptor.attach("NewObjectArray", h), e.JNIInterceptor.attach("GetObjectArrayElement", h), 
e.JNIInterceptor.attach("SetObjectArrayElement", h), e.JNIInterceptor.attach("NewBooleanArray", h), 
e.JNIInterceptor.attach("NewByteArray", h), e.JNIInterceptor.attach("NewCharArray", h), 
e.JNIInterceptor.attach("NewShortArray", h), e.JNIInterceptor.attach("NewIntArray", h), 
e.JNIInterceptor.attach("NewLongArray", h), e.JNIInterceptor.attach("NewFloatArray", h), 
e.JNIInterceptor.attach("NewDoubleArray", h), e.JNIInterceptor.attach("GetBooleanArrayElements", h), 
e.JNIInterceptor.attach("GetByteArrayElements", h), e.JNIInterceptor.attach("GetCharArrayElements", h), 
e.JNIInterceptor.attach("GetShortArrayElements", h), e.JNIInterceptor.attach("GetIntArrayElements", h), 
e.JNIInterceptor.attach("GetLongArrayElements", h), e.JNIInterceptor.attach("GetFloatArrayElements", h), 
e.JNIInterceptor.attach("GetDoubleArrayElements", h), e.JNIInterceptor.attach("ReleaseBooleanArrayElements", h), 
e.JNIInterceptor.attach("ReleaseByteArrayElements", h), e.JNIInterceptor.attach("ReleaseCharArrayElements", h), 
e.JNIInterceptor.attach("ReleaseShortArrayElements", h), e.JNIInterceptor.attach("ReleaseIntArrayElements", h), 
e.JNIInterceptor.attach("ReleaseLongArrayElements", h), e.JNIInterceptor.attach("ReleaseFloatArrayElements", h), 
e.JNIInterceptor.attach("ReleaseDoubleArrayElements", h), e.JNIInterceptor.attach("GetBooleanArrayRegion", h), 
e.JNIInterceptor.attach("GetByteArrayRegion", h), e.JNIInterceptor.attach("GetCharArrayRegion", h), 
e.JNIInterceptor.attach("GetShortArrayRegion", h), e.JNIInterceptor.attach("GetIntArrayRegion", h), 
e.JNIInterceptor.attach("GetLongArrayRegion", h), e.JNIInterceptor.attach("GetFloatArrayRegion", h), 
e.JNIInterceptor.attach("GetDoubleArrayRegion", h), e.JNIInterceptor.attach("SetBooleanArrayRegion", h), 
e.JNIInterceptor.attach("SetByteArrayRegion", h), e.JNIInterceptor.attach("SetCharArrayRegion", h), 
e.JNIInterceptor.attach("SetShortArrayRegion", h), e.JNIInterceptor.attach("SetIntArrayRegion", h), 
e.JNIInterceptor.attach("SetLongArrayRegion", h), e.JNIInterceptor.attach("SetFloatArrayRegion", h), 
e.JNIInterceptor.attach("SetDoubleArrayRegion", h), e.JNIInterceptor.attach("RegisterNatives", h), 
e.JNIInterceptor.attach("UnregisterNatives", h), e.JNIInterceptor.attach("MonitorEnter", h), 
e.JNIInterceptor.attach("MonitorExit", h), e.JNIInterceptor.attach("GetJavaVM", h), 
e.JNIInterceptor.attach("GetStringRegion", h), e.JNIInterceptor.attach("GetStringUTFRegion", h), 
e.JNIInterceptor.attach("GetPrimitiveArrayCritical", h), e.JNIInterceptor.attach("ReleasePrimitiveArrayCritical", h), 
e.JNIInterceptor.attach("GetStringCritical", h), e.JNIInterceptor.attach("ReleaseStringCritical", h), 
e.JNIInterceptor.attach("NewWeakGlobalRef", h), e.JNIInterceptor.attach("DeleteWeakGlobalRef", h), 
e.JNIInterceptor.attach("ExceptionCheck", h), e.JNIInterceptor.attach("NewDirectByteBuffer", h), 
e.JNIInterceptor.attach("GetDirectBufferAddress", h), e.JNIInterceptor.attach("GetDirectBufferCapacity", h), 
e.JNIInterceptor.attach("GetObjectRefType", h);

},{"./transport/data_transport":2,"./utils/method_data":3,"jnitrace-engine":8}],2:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.DataTransport = void 0;

const t = require("../utils/types"), e = require("jnitrace-engine"), s = 0, r = 0, a = -1, i = 1, n = 0, g = 0, d = 0;

class h {
  constructor(t, e, s) {
    this.name = {}, this.sig = {}, this.addr = {}, this.name = t, this.sig = e, this.addr = s;
  }
}

class l {
  constructor(t, e, s) {
    this.value = t, null !== e && (e instanceof ArrayBuffer || (this.data = e)), void 0 !== s && (-1 === s ? this.has_data = !0 : this.data_for = s);
  }
  getMetadata() {
    return this.metadata;
  }
  setMetadata(t) {
    this.metadata = t;
  }
}

class o {
  constructor(t, e, s) {
    this.address = t, this.module = e, this.symbol = s;
  }
}

class u {
  constructor(t, e, s, r, a, i, n, g) {
    this.type = "trace_data", this.call_type = t, this.method = e, this.args = s, this.ret = r, 
    this.thread_id = a, this.timestamp = i, this.java_params = n, this.backtrace = g;
  }
}

class c {
  constructor() {
    this.start = Date.now(), this.byteArraySizes = new Map, this.jobjects = new Map, 
    this.jfieldIDs = new Map, this.jmethodIDs = new Map, this.jstrings = new Map, this.include = [], 
    this.exclude = [];
  }
  setIncludeFilter(t) {
    this.include = t;
  }
  setExcludeFilter(t) {
    this.exclude = t;
  }
  reportJavaVMCall(t, s) {
    const r = e.Config.getInstance(), a = [], i = new l(t.ret, null), n = t.getArgAsPtr(0);
    if (!r.vm || this.shouldIgnoreMethod(t)) return;
    a.push(new l(n, null));
    const g = this.addJavaVMArgs(t, a);
    this.sendToHost("JavaVM", t, a, i, g, s);
  }
  reportJNIEnvCall(t, s) {
    const r = e.Config.getInstance(), a = [], i = [], n = t.getArgAsPtr(0);
    this.updateState(t), a.push(new l(n, null));
    let g = null;
    const d = this.addJNIEnvArgs(t, a), h = this.addJNIEnvRet(t, i);
    null !== d && null === h ? g = d : null == d && null !== h && (g = h), this.enrichTraceData(t, a, i), 
    r.env && !this.shouldIgnoreMethod(t) && this.sendToHost("JNIEnv", t, a, i[0], g, s);
  }
  updateArrayLengths(t, e) {
    e ? this.byteArraySizes.set(t.args[1].toString(), t.ret) : this.byteArraySizes.set(t.ret.toString(), t.args[1]);
  }
  updateMethodIDs(t) {
    const e = t.ret.toString(), s = t.args[2].readCString(), r = t.args[3].readCString();
    null !== s && null !== r && this.jmethodIDs.set(e, s + r);
  }
  updateFieldIDs(t) {
    const e = t.ret.toString(), s = t.args[2].readCString(), r = t.args[3].readCString();
    null !== s && null !== r && this.jfieldIDs.set(e, s + ":" + r);
  }
  updateClassIDs(t) {
    const e = t.ret.toString(), s = t.args[1].readCString();
    null !== s && this.jobjects.set(e, s);
  }
  updateObjectIDsFromRefs(t, e) {
    if (e) {
      const e = t.ret.toString(), s = t.args[1].toString();
      this.jobjects.has(s) && this.jobjects.set(e, this.jobjects.get(s));
    } else {
      const e = t.args[1].toString();
      this.jobjects.delete(e);
    }
  }
  updateObjectIDsFromClass(t) {
    const e = t.args[1].toString(), s = t.ret.toString();
    this.jobjects.has(e) && this.jobjects.set(s, e);
  }
  updateObjectIDsFromCall(e) {
    if (void 0 !== e.javaMethod) {
      let s = 4;
      const r = e.method.args[3];
      [ "jvalue*", "va_list" ].includes(r) && (s = 5);
      for (let r = s; r < e.args.length; r++) {
        const a = e.args[r].toString();
        if (this.jobjects.has(a)) continue;
        const i = e.javaMethod.nativeParams[r - s];
        t.Types.isComplexObjectType(i) && this.jobjects.set(a, i.slice(1, -1));
      }
      e.method.name.includes("Object") && (this.jobjects.has(e.ret.toString()) || this.jobjects.set(e.ret.toString(), e.javaMethod.ret.slice(1, -1)));
    }
  }
  updateStringIDs(t) {
    const e = t.getArgAsPtr(1).readUtf8String();
    null !== e && this.jstrings.set(t.ret.toString(), e);
  }
  updateState(t) {
    const e = t.method.name;
    "GetArrayLength" === e ? this.updateArrayLengths(t, !0) : e.startsWith("New") && e.endsWith("Array") ? this.updateArrayLengths(t, !1) : [ "GetMethodID", "GetStaticMethodID" ].includes(e) ? this.updateMethodIDs(t) : [ "GetFieldID", "GetStaticFieldID" ].includes(e) ? this.updateFieldIDs(t) : [ "FindClass", "DefineClass" ].includes(e) ? this.updateClassIDs(t) : e.startsWith("New") && e.endsWith("Ref") ? this.updateObjectIDsFromRefs(t, !0) : e.startsWith("Delete") && e.endsWith("Ref") ? this.updateObjectIDsFromRefs(t, !1) : "GetObjectClass" === e ? this.updateObjectIDsFromClass(t) : e.startsWith("Call") ? this.updateObjectIDsFromCall(t) : "NewStringUTF" === e && this.updateStringIDs(t);
  }
  shouldIgnoreMethod(t) {
    const e = t.method.name;
    if (this.include.length > 0) {
      if (0 === this.include.filter((t => new RegExp(t).test(e))).length) return !0;
    }
    if (this.exclude.length > 0) {
      if (this.exclude.filter((t => new RegExp(t).test(e))).length > 0) return !0;
    }
    return !1;
  }
  enrichSingleItem(e, s, r) {
    t.Types.isComplexObjectType(e) ? this.jobjects.has(s) && r.setMetadata(this.jobjects.get(s)) : "jmethodID" === e ? this.jmethodIDs.has(s) && r.setMetadata(this.jmethodIDs.get(s)) : "jfieldID" === e ? this.jfieldIDs.has(s) && r.setMetadata(this.jfieldIDs.get(s)) : "jstring" === e && this.jstrings.has(s) && r.setMetadata(this.jstrings.get(s));
  }
  enrichTraceData(t, e, s) {
    let r = 0;
    for (;r < t.method.args.length; r++) if ([ "jvalue*, va_list" ].includes(t.method.args[r])) r++; else {
      if ("..." === t.method.args[r]) break;
      this.enrichSingleItem(t.method.args[r], t.args[r].toString(), e[r]);
    }
    const a = r;
    for (;r < e.length; r++) void 0 !== t.javaMethod && this.enrichSingleItem(t.javaMethod.nativeParams[r - a], t.args[r].toString(), e[r]);
    void 0 !== t.ret && this.enrichSingleItem(t.method.ret, t.ret.toString(), s[0]);
  }
  addDefineClassArgs(t, e) {
    const s = t.getArgAsPtr(1).readCString();
    e.push(new l(t.args[1], s)), e.push(new l(t.args[2], null));
    const r = t.getArgAsPtr(3), a = t.getArgAsNum(4), i = r.readByteArray(a);
    return e.push(new l(t.args[3], null, 3)), e.push(new l(t.args[4], null)), i;
  }
  addFindClassArgs(t, e) {
    const s = t.getArgAsPtr(1).readCString();
    e.push(new l(t.args[1], s));
  }
  addThrowNewArgs(t, e) {
    const s = t.getArgAsPtr(2).readCString();
    e.push(new l(t.args[1], null)), e.push(new l(t.args[2], s));
  }
  addFatalErrorArgs(t, e) {
    const s = t.getArgAsPtr(1).readCString();
    e.push(new l(t.args[1], s));
  }
  addGetGenericIDArgs(t, e) {
    const s = t.getArgAsPtr(2).readCString(), r = t.getArgAsPtr(3).readCString();
    e.push(new l(t.args[1], null)), e.push(new l(t.args[2], s)), e.push(new l(t.args[3], r));
  }
  addNewStringArgs(t, e) {
    const s = t.getArgAsPtr(1), r = t.getArgAsNum(2), a = s.readByteArray(r);
    return e.push(new l(t.args[1], null, 1)), e.push(new l(t.args[2], null)), a;
  }
  addGetGenericBufferArgs(t, e) {
    e.push(new l(t.args[1], null)), t.getArgAsPtr(2).isNull() ? e.push(new l(t.args[2], null)) : e.push(new l(t.args[2], t.getArgAsPtr(2).readS8()));
  }
  addReleaseCharsArgs(t, e) {
    const s = t.getArgAsPtr(2).readCString();
    e.push(new l(t.args[2], null)), e.push(new l(t.args[2], s));
  }
  addGetGenericBufferRegionArgs(e, s) {
    const r = e.method.args[4].slice(0, -1), a = t.Types.convertNativeJTypeToFridaType(r), i = t.Types.sizeOf(a), n = e.getArgAsPtr(4), g = e.getArgAsNum(3), d = n.readByteArray(g * i), h = e.args.length - 1;
    for (let t = 1; t < h; t++) s.push(new l(e.args[t], null));
    return s.push(new l(e.args[e.args.length - 1], null, e.args.length - 1)), d;
  }
  addNewStringUTFArgs(t, e) {
    const s = t.getArgAsPtr(1).readUtf8String();
    e.push(new l(t.args[1], s));
  }
  addRegisterNativesArgs(t, e) {
    const s = t.getArgAsNum(3), r = [];
    e.push(new l(t.args[1], null));
    for (let e = 0; e < 3 * s; e += 3) {
      const s = t.getArgAsPtr(2), a = s.add(e * Process.pointerSize).readPointer(), i = a.readCString(), n = 1, g = s.add((e + n) * Process.pointerSize).readPointer(), d = g.readCString(), l = 2, o = s.add((e + l) * Process.pointerSize).readPointer();
      r.push(new h({
        value: a.toString(),
        data: i
      }, {
        value: g.toString(),
        data: d
      }, {
        value: o.toString()
      }));
    }
    e.push(new l(t.args[2], r)), e.push(new l(t.args[3], null));
  }
  addGetJavaVMArgs(t, e) {
    e.push(new l(t.args[1], t.getArgAsPtr(1).readPointer()));
  }
  addReleaseStringCriticalArgs(t, e) {
    e.push(new l(t.args[1], null)), e.push(new l(t.args[2], t.getArgAsPtr(1).readCString()));
  }
  addReleaseElementsArgs(e, s) {
    const r = e.method.args[2].slice(0, -1), a = t.Types.convertNativeJTypeToFridaType(r), i = t.Types.sizeOf(a), n = e.getArgAsPtr(2), g = e.getArgAsPtr(1).toString(), d = this.byteArraySizes.get(g);
    let h = null;
    void 0 !== d && (h = n.readByteArray(d * i));
    for (let t = 1; t < e.args.length; t++) {
      const r = e.args[t];
      let a;
      2 === t && (a = t), s.push(new l(r, null, a));
    }
    return h;
  }
  addGenericArgs(t, e) {
    for (let s = 1; s < t.args.length; s++) e.push(new l(t.args[s], null));
  }
  addJNIEnvArgs(t, e) {
    const s = t.method.name;
    if ("DefineClass" === s) return this.addDefineClassArgs(t, e);
    if ("FindClass" === s) this.addFindClassArgs(t, e); else if ("ThrowNew" === s) this.addThrowNewArgs(t, e); else if ("FatalError" === s) this.addFatalErrorArgs(t, e); else if (s.endsWith("ID")) this.addGetGenericIDArgs(t, e); else {
      if ("NewString" === s) return this.addNewStringArgs(t, e);
      if (s.startsWith("Get") && s.endsWith("Chars") || s.startsWith("Get") && s.endsWith("Elements") || s.startsWith("Get") && s.endsWith("ArrayCritical") || "GetStringCritical" === s) this.addGetGenericBufferArgs(t, e); else if (s.startsWith("Release") && s.endsWith("Chars")) this.addReleaseCharsArgs(t, e); else {
        if (s.endsWith("Region")) return this.addGetGenericBufferRegionArgs(t, e);
        if ("NewStringUTF" === s) this.addNewStringUTFArgs(t, e); else if ("RegisterNatives" === s) this.addRegisterNativesArgs(t, e); else if ("GetJavaVM" === s) this.addGetJavaVMArgs(t, e); else if ("ReleaseStringCritical" === s) this.addReleaseStringCriticalArgs(t, e); else {
          if (s.startsWith("Release") && s.endsWith("Elements") || s.startsWith("Release") && s.endsWith("ArrayCritical")) return this.addReleaseElementsArgs(t, e);
          this.addGenericArgs(t, e);
        }
      }
    }
    return null;
  }
  addJNIEnvRet(e, s) {
    const r = e.method.name;
    if (r.startsWith("Get") && r.endsWith("Elements") || r.startsWith("Get") && r.endsWith("ArrayCritical")) {
      const r = e.args[1].toString();
      if (this.byteArraySizes.has(r)) {
        const r = e.method.ret.slice(0, -1), a = t.Types.convertNativeJTypeToFridaType(r), i = t.Types.sizeOf(a), n = e.ret, g = this.byteArraySizes.get(e.getArgAsPtr(1).toString());
        return s.push(new l(e.ret, null, -1)), n.readByteArray(g * i);
      }
    }
    return s.push(new l(e.ret, null)), null;
  }
  addAttachCurrentThreadArgs(e, s) {
    const r = t.Types.sizeOf("pointer") + t.Types.sizeOf("pointer") + 4, a = e.args[1];
    let i = null;
    0 === e.ret ? i = e.getArgAsPtr(1).readPointer() : e.getArgAsPtr(1).isNull() || (i = e.getArgAsPtr(1).readPointer()), 
    s.push(new l(a, i));
    const n = e.args[2];
    return e.getArgAsPtr(2).isNull() ? (s.push(new l(n, null)), null) : (s.push(new l(n, null, 2)), 
    e.getArgAsPtr(2).readByteArray(r));
  }
  addGetEnvArgs(t, e) {
    const s = t.args[1];
    let r = null;
    0 === t.ret ? r = t.getArgAsPtr(1).readPointer() : t.getArgAsPtr(1).isNull() || (r = t.getArgAsPtr(1).readPointer()), 
    e.push(new l(s, r)), e.push(new l(t.args[2], null));
  }
  addJavaVMArgs(t, e) {
    const s = t.method.name;
    return s.startsWith("AttachCurrentThread") ? this.addAttachCurrentThreadArgs(t, e) : ("GetEnv" === s && this.addGetEnvArgs(t, e), 
    null);
  }
  createBacktrace(t, e) {
    let s = t;
    if (!(s instanceof Array)) {
      let r = null;
      r = "fuzzy" === e ? Backtracer.FUZZY : Backtracer.ACCURATE, s = Thread.backtrace(t, r);
    }
    return s.map((t => new o(t, Process.findModuleByAddress(t), DebugSymbol.fromAddress(t))));
  }
  sendToHost(t, s, r, a, i, n) {
    const g = e.Config.getInstance(), d = s.jParams;
    let h;
    void 0 !== n && (h = this.createBacktrace(n, g.backtrace));
    const l = new u(t, s.method, r, a, Process.getCurrentThreadId(), Date.now() - this.start, d, h);
    send(l, i);
  }
}

exports.DataTransport = c;

},{"../utils/types":4,"jnitrace-engine":8}],3:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.MethodData = void 0;

class t {
  constructor(t, e, r, s) {
    this._method = t, this._jmethod = s, this._args = e, this._ret = r, this._jparams = void 0 === s ? [] : s.nativeParams;
  }
  get method() {
    return this._method;
  }
  get javaMethod() {
    return this._jmethod;
  }
  get args() {
    return this._args;
  }
  getArgAsPtr(t) {
    return this._args[t];
  }
  getArgAsNum(t) {
    return this._args[t];
  }
  get jParams() {
    return this._jparams;
  }
  get ret() {
    return this._ret;
  }
}

exports.MethodData = t;

},{}],4:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.Types = void 0;

const t = 1, e = 8, j = 1, o = {
  isComplexObjectType: t => [ "jobject", "jclass", "jweak" ].includes(t),
  sizeOf: t => "double" === t || "float" === t || "int64" === t ? 8 : "char" === t ? 1 : Process.pointerSize,
  convertNativeJTypeToFridaType: t => t.endsWith("*") || "va_list" === t || "jmethodID" === t || "jfieldID" === t ? "pointer" : "va_list" === t ? "va_list" : ("jweak" === t && (t = "jobject"), 
  "jthrowable" === t && (t = "jobject"), t.includes("Array") && (t = "jarray"), "jarray" === t && (t = "jobject"), 
  "jstring" === t && (t = "jobject"), "jclass" === t && (t = "jobject"), "jobject" === t ? "pointer" : ("jsize" === t && (t = "jint"), 
  "jdouble" === t ? "double" : "jfloat" === t ? "float" : "jchar" === t ? "uint16" : "jboolean" === t ? "char" : "jlong" === t ? "int64" : "jint" === t ? "int" : "jshort" === t ? "int16" : "jbyte" === t ? "char" : t)),
  convertJTypeToNativeJType(t) {
    let e = "", j = !1;
    return t.startsWith("[") && (j = !0, t = t.substring(1)), "B" === t ? e += "jbyte" : "S" === t ? e += "jshort" : "I" === t ? e += "jint" : "J" === t ? e += "jlong" : "F" === t ? e += "jfloat" : "D" === t ? e += "jdouble" : "C" === t ? e += "jchar" : "Z" === t ? e += "jboolean" : t.startsWith("L") && (e += "Ljava/lang/String;" === t ? "jstring" : "Ljava/lang/Class;" === t ? "jclass" : "jobject"), 
    j && ("jstring" === e && (e = "jobject"), e += "Array"), e;
  }
};

exports.Types = o;

},{}],5:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": "void"
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": "void"
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": "void"
    },
    {
        "name": "DestroyJavaVM",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThread",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    },
    {
        "name": "DetachCurrentThread",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "GetEnv",
        "args": [
            "JavaVM*",
            "void**",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThreadAsDaemon",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    }
]

},{}],6:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": "void"
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": "void"
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": "void"
    },
    {
        "name": "reserved3",
        "args": [],
        "ret": "void"
    },
    {
        "name": "GetVersion",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jint"
    },
    {
        "name": "DefineClass",
        "args": [
            "JNIEnv*",
            "char*",
            "jobject",
            "jbyte*",
            "jsize"
        ],
        "ret": "jclass"
    },
    {
        "name": "FindClass",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jclass"
    },
    {
        "name": "FromReflectedMethod",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "FromReflectedField",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "ToReflectedMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetSuperclass",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsAssignableFrom",
        "args": [
            "JNIEnv*",
            "jclass",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "ToReflectedField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "Throw",
        "args": [
            "JNIEnv*",
            "jthrowable"
        ],
        "ret": "jint"
    },
    {
        "name": "ThrowNew",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*"
        ],
        "ret": "jint"
    },
    {
        "name": "ExceptionOccurred",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jthrowable"
    },
    {
        "name": "ExceptionDescribe",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionClear",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "FatalError",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "PushLocalFrame",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "PopLocalFrame",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "DeleteGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "DeleteLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "IsSameObject",
        "args": [
            "JNIEnv*",
            "jobject",
            "jobject"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "EnsureLocalCapacity",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AllocObject",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObject",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetObjectClass",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsInstanceOf",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallStaticObjectMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticBooleanMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticByteMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticCharMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticShortMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticIntMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticLongMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticFloatMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticDoubleMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticVoidMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "NewString",
        "args": [
            "JNIEnv*",
            "jchar*",
            "jsize"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar*"
    },
    {
        "name": "ReleaseStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewStringUTF",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringUTFLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "char*"
    },
    {
        "name": "ReleaseStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetArrayLength",
        "args": [
            "JNIEnv*",
            "jarray"
        ],
        "ret": "jsize"
    },
    {
        "name": "NewObjectArray",
        "args": [
            "JNIEnv*",
            "jsize",
            "jclass",
            "jobject"
        ],
        "ret": "jobjectArray"
    },
    {
        "name": "GetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize"
        ],
        "ret": "jobject"
    },
    {
        "name": "SetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "NewBooleanArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbooleanArray"
    },
    {
        "name": "NewByteArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbyteArray"
    },
    {
        "name": "NewCharArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jcharArray"
    },
    {
        "name": "NewShortArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jshortArray"
    },
    {
        "name": "NewIntArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jintArray"
    },
    {
        "name": "NewLongArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jlongArray"
    },
    {
        "name": "NewFloatArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jfloatArray"
    },
    {
        "name": "NewDoubleArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jdoubleArray"
    },
    {
        "name": "GetBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*"
        ],
        "ret": "jboolean*"
    },
    {
        "name": "GetByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jboolean*"
        ],
        "ret": "jbyte*"
    },
    {
        "name": "GetCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jboolean*"
        ],
        "ret": "jchar*"
    },
    {
        "name": "GetShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jboolean*"
        ],
        "ret": "jshort*"
    },
    {
        "name": "GetIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jboolean*"
        ],
        "ret": "jint*"
    },
    {
        "name": "GetLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jboolean*"
        ],
        "ret": "jlong*"
    },
    {
        "name": "GetFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jboolean*"
        ],
        "ret": "jfloat*"
    },
    {
        "name": "GetDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jboolean*"
        ],
        "ret": "jdouble*"
    },
    {
        "name": "ReleaseBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jbyte*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jchar*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jshort*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jint*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jlong*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jfloat*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jdouble*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "GetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "GetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "GetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "GetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "GetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "RegisterNatives",
        "args": [
            "JNIEnv*",
            "jclass",
            "JNINativeMethod*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "UnregisterNatives",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorEnter",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorExit",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "GetJavaVM",
        "args": [
            "JNIEnv*",
            "JavaVM**"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStringRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringUTFRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetPrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "ReleasePrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "void*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "ReleaseStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jweak"
    },
    {
        "name": "DeleteWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jweak"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionCheck",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewDirectByteBuffer",
        "args": [
            "JNIEnv*",
            "void*",
            "jlong"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetDirectBufferAddress",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "GetDirectBufferCapacity",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetObjectRefType",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobjectRefType"
    }
]

},{}],7:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.run = void 0;

const e = require("./utils/reference_manager"), t = require("./utils/config"), n = require("./jni/x86/jni_env_interceptor_x86"), r = require("./jni/x64/jni_env_interceptor_x64"), i = require("./jni/arm/jni_env_interceptor_arm"), o = require("./jni/arm64/jni_env_interceptor_arm64"), s = require("./jni/java_vm_interceptor"), a = require("./jni/jni_thread_manager"), l = require(".");

function c(c) {
  const u = new a.JNIThreadManager, d = new e.ReferenceManager;
  let h;
  if ("ia32" === Process.arch ? h = new n.JNIEnvInterceptorX86(d, u, c) : "x64" === Process.arch ? h = new r.JNIEnvInterceptorX64(d, u, c) : "arm" === Process.arch ? h = new i.JNIEnvInterceptorARM(d, u, c) : "arm64" === Process.arch && (h = new o.JNIEnvInterceptorARM64(d, u, c)), 
  void 0 === h) throw new Error(Process.arch + " currently unsupported, please file an issue.");
  const p = new s.JavaVMInterceptor(d, u, h, c);
  h.setJavaVMInterceptor(p);
  const f = new Map, g = new Map;
  function v(e) {
    let n = !1;
    if (null === e) return !1;
    l.JNILibraryWatcher.doCallback(e);
    const r = t.Config.getInstance();
    return 1 === r.libraries.length && "*" === r.libraries[0] && (n = !0), n || (n = r.libraries.filter((t => e.includes(t))).length > 0), 
    n;
  }
  function I(e) {
    return Interceptor.attach(e, {
      onEnter(e) {
        if (void 0 === h) return;
        const t = this.threadId, n = ptr(e[0].toString());
        let r = NULL;
        u.setJNIEnv(t, n), r = h.isInitialised() ? h.get() : h.create(), e[0] = r;
      }
    });
  }
  const _ = Module.findExportByName(null, "dlopen"), N = Module.findExportByName(null, "dlsym"), m = Module.findExportByName(null, "dlclose");
  if (null !== _ && null !== N && null !== m) {
    const e = 0, n = new NativeFunction(_, "pointer", [ "pointer", "int" ]);
    Interceptor.replace(n, new NativeCallback(((e, t) => {
      const r = e.readCString(), i = n(e, t);
      return null !== r && (v(r) ? f.set(i.toString(), !0) : g.set(i.toString(), !0)), 
      i;
    }), "pointer", [ "pointer", "int" ]));
    const r = new NativeFunction(N, "pointer", [ "pointer", "pointer" ]);
    Interceptor.attach(r, {
      onEnter(t) {
        this.handle = ptr(t[e].toString()), g.has(this.handle) || (this.symbol = t[1].readCString());
      },
      onLeave(n) {
        if (n.isNull() || g.has(this.handle)) return;
        const r = t.Config.getInstance();
        if (r.includeExport.length > 0) {
          if (0 === r.includeExport.filter((e => this.symbol.includes(e))).length) return;
        }
        if (r.excludeExport.length > 0) {
          if (r.excludeExport.filter((e => this.symbol.includes(e))).length > 0) return;
        }
        if (!f.has(this.handle)) {
          const e = Process.findModuleByAddress(n);
          null !== e && v(e.path) && f.set(this.handle, !0);
        }
        if (f.has(this.handle)) {
          const e = this.symbol;
          "JNI_OnLoad" === e ? (i = ptr(n.toString()), Interceptor.attach(i, {
            onEnter(e) {
              let t = NULL;
              const n = ptr(e[0].toString());
              u.hasJavaVM() || u.setJavaVM(n), t = p.isInitialised() ? p.get() : p.create(), e[0] = t;
            }
          })) : e.startsWith("Java_") && I(ptr(n.toString()));
        } else {
          let t = r.libraries[e];
          if ("*" !== t) {
            const e = Process.findModuleByAddress(n);
            if (null === e) return;
            t = e.name;
          }
          if (null === /lib.+\.so/.exec(t)) return;
          (r.libraries.includes(t) || "*" === t) && I(ptr(n.toString()));
        }
        var i;
      }
    });
    const i = new NativeFunction(m, "int", [ "pointer" ]);
    Interceptor.attach(i, {
      onEnter(t) {
        const n = t[e].toString();
        f.has(n) && (this.handle = n);
      },
      onLeave(e) {
        void 0 !== this.handle && e.isNull() && f.delete(this.handle);
      }
    });
  }
}

exports.run = c;

},{".":8,"./jni/arm/jni_env_interceptor_arm":10,"./jni/arm64/jni_env_interceptor_arm64":11,"./jni/java_vm_interceptor":13,"./jni/jni_thread_manager":16,"./jni/x64/jni_env_interceptor_x64":17,"./jni/x86/jni_env_interceptor_x86":18,"./utils/config":19,"./utils/reference_manager":22}],8:[function(require,module,exports){
"use strict";

var e = this && this.__importDefault || function(e) {
  return e && e.__esModule ? e : {
    default: e
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JavaMethod = exports.JNIMethod = exports.ConfigBuilder = exports.Config = exports.JNIInvocationListener = exports.JNINativeReturnValue = exports.JNILibraryWatcher = exports.JNIInterceptor = void 0;

const t = require("./utils/config");

Object.defineProperty(exports, "Config", {
  enumerable: !0,
  get: function() {
    return t.Config;
  }
});

const r = require("./utils/config_builder");

Object.defineProperty(exports, "ConfigBuilder", {
  enumerable: !0,
  get: function() {
    return r.ConfigBuilder;
  }
});

const n = require("./internal/jni_callback_manager"), o = require("./jni/jni_method");

Object.defineProperty(exports, "JNIMethod", {
  enumerable: !0,
  get: function() {
    return o.JNIMethod;
  }
});

const a = require("./utils/java_method");

Object.defineProperty(exports, "JavaMethod", {
  enumerable: !0,
  get: function() {
    return a.JavaMethod;
  }
});

const i = e(require("./data/jni_env.json")), l = e(require("./data/java_vm.json")), u = require("./engine"), s = new n.JNICallbackManager;

class c {
  constructor(e) {
    this.value = e;
  }
  get() {
    return this.value;
  }
  replace(e) {
    this.value = e;
  }
}

exports.JNINativeReturnValue = c;

class d {
  constructor(e, t) {
    this.callbacks = e, this.method = t;
  }
  detach() {
    this.callbacks.has(this.method) && this.callbacks.delete(this.method);
  }
}

var f, h;

exports.JNIInvocationListener = d, function(e) {
  let t = s;
  e.attach = function(e, r) {
    for (let n = 4; n < i.default.length; n++) {
      if (i.default[n].name === e) return t.addCallback(e, r);
    }
    for (let n = 3; n < l.default.length; n++) {
      if (l.default[n].name === e) return t.addCallback(e, r);
    }
    throw new Error("Method name (" + e + ") is not a valid JNI method.");
  }, e.detatchAll = function() {
    t.clear();
  };
}(f || (f = {})), exports.JNIInterceptor = f, function(e) {
  let t;
  e.setCallback = function(e) {
    t = e;
  }, e.doCallback = function(e) {
    void 0 !== t?.onLoaded && t.onLoaded(e);
  };
}(h || (h = {})), exports.JNILibraryWatcher = h, u.run(s);

},{"./data/java_vm.json":5,"./data/jni_env.json":6,"./engine":7,"./internal/jni_callback_manager":9,"./jni/jni_method":15,"./utils/config":19,"./utils/config_builder":20,"./utils/java_method":21}],9:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNICallbackManager = void 0;

const a = require(".."), e = require("..");

class l {
  constructor() {
    this.callbacks = new Map;
  }
  addCallback(e, l) {
    if (this.callbacks.has(e)) throw new Error("Callback already exists for " + e + " please detach first.");
    return this.callbacks.set(e, l), new a.JNIInvocationListener(this.callbacks, e);
  }
  doBeforeCallback(a, e, l) {
    if (this.callbacks.has(a)) {
      const s = this.callbacks.get(a);
      void 0 !== s?.onEnter && s.onEnter.call(e, l);
    }
  }
  doAfterCallback(a, l, s) {
    if (this.callbacks.has(a)) {
      const t = this.callbacks.get(a);
      if (void 0 !== t?.onLeave) {
        const a = new e.JNINativeReturnValue(s);
        t.onLeave.call(l, a), a.get() !== s && (s = a.get());
      }
    }
    return s;
  }
  clear() {
    this.callbacks.clear();
  }
}

exports.JNICallbackManager = l;

},{"..":8}],10:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNIEnvInterceptorARM = void 0;

const t = require("../jni_env_interceptor"), s = require("../../utils/types");

class e extends t.JNIEnvInterceptor {
  constructor(t, s, e) {
    super(t, s, e), this.vaList = NULL, this.vaListOffset = 0;
  }
  createStubFunction() {
    const t = Memory.alloc(Process.pageSize);
    return Memory.patchCode(t, Process.pageSize, (s => {
      const e = new ArmWriter(s, {
        pc: t
      });
      e.putInstruction(3844988932);
      e.putInstruction(3835555844);
    })), t;
  }
  buildVaArgParserShellcode(t, s, e) {
    t.add(1024).writePointer(e), Memory.patchCode(t, Process.pageSize, (s => {
      const e = new ArmWriter(s, {
        pc: t
      });
      e.putNop(), e.putNop(), e.putNop(), e.putNop();
      e.putInstruction(3851355136);
      e.putInstruction(3851359232);
      e.putInstruction(3851363328);
      e.putInstruction(3851367424);
      e.putInstruction(3851412480);
      e.putInstruction(3852403668);
      const r = 3778019120;
      e.putInstruction(r);
      e.putInstruction(3852407784);
      e.putInstruction(3852411880);
      e.putInstruction(3852415976), e.putInstruction(r);
      e.putInstruction(3852407780);
      e.putInstruction(3778019089), e.flush();
    }));
  }
  setUpVaListArgExtract(t) {
    this.vaList = t, this.vaListOffset = 0;
  }
  extractVaListArgValue(t, e) {
    const r = this.vaList.add(this.vaListOffset);
    return this.vaListOffset += s.Types.sizeOf(t.fridaParams[e]), r;
  }
  resetVaListArgExtract() {
    this.vaList = NULL, this.vaListOffset = 0;
  }
}

exports.JNIEnvInterceptorARM = e;

},{"../../utils/types":23,"../jni_env_interceptor":14}],11:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNIEnvInterceptorARM64 = void 0;

const t = require("../jni_env_interceptor");

class s extends t.JNIEnvInterceptor {
  constructor(t, s, e) {
    super(t, s, e), this.stack = NULL, this.stackIndex = 0, this.grTop = NULL, this.vrTop = NULL, 
    this.grOffs = 0, this.grOffsIndex = 0, this.vrOffs = 0, this.vrOffsIndex = 0;
  }
  createStubFunction() {
    const t = Memory.alloc(Process.pageSize);
    return Memory.patchCode(t, Process.pageSize, (s => {
      new Arm64Writer(s, {
        pc: t
      }).putInstruction(3596551104);
    })), t;
  }
  buildVaArgParserShellcode(t, s, e) {
    t.add(1024).writePointer(e), Memory.patchCode(t, Process.pageSize, (s => {
      const e = new Arm64Writer(s, {
        pc: t
      }), r = 2415919104;
      e.putInstruction(r);
      for (let t = 1; t < 31; t++) {
        let s = 4177526784;
        s += t;
        s += (1032 + t * Process.pointerSize) / 2 << 8, e.putInstruction(s);
      }
      e.putInstruction(4181852160);
      const i = 3594452992;
      e.putInstruction(i), e.putPushRegReg("x0", "sp"), e.putInstruction(r);
      for (let t = 1; t < 30; t++) {
        let s = 4181721088;
        s += t;
        s += (1032 + t * Process.pointerSize) / 2 << 8, e.putInstruction(s);
      }
      e.putPopRegReg("x0", "sp"), e.putInstruction(i);
      e.putInstruction(2415919105);
      e.putInstruction(4181883938);
      e.putInstruction(3592355904), e.flush();
    }));
  }
  setUpVaListArgExtract(t) {
    this.stack = t.readPointer(), this.stackIndex = 0, this.grTop = t.add(Process.pointerSize).readPointer(), 
    this.vrTop = t.add(2 * Process.pointerSize).readPointer(), this.grOffs = t.add(3 * Process.pointerSize).readS32(), 
    this.grOffsIndex = 0, this.vrOffs = t.add(3 * Process.pointerSize + 4).readS32(), 
    this.vrOffsIndex = 0;
  }
  extractVaListArgValue(t, s) {
    let e = NULL;
    return "float" === t.fridaParams[s] || "double" === t.fridaParams[s] ? this.vrOffsIndex < 8 ? (e = this.vrTop.add(this.vrOffs).add(this.vrOffsIndex * Process.pointerSize * 2), 
    this.vrOffsIndex++) : (e = this.stack.add(this.stackIndex * Process.pointerSize), 
    this.stackIndex++) : this.grOffsIndex < 4 ? (e = this.grTop.add(this.grOffs).add(this.grOffsIndex * Process.pointerSize), 
    this.grOffsIndex++) : (e = this.stack.add(this.stackIndex * Process.pointerSize), 
    this.stackIndex++), e;
  }
  resetVaListArgExtract() {
    this.stack = NULL, this.stackIndex = 0, this.grTop = NULL, this.vrTop = NULL, this.grOffs = 0, 
    this.grOffsIndex = 0, this.vrOffs = 0, this.vrOffsIndex = 0;
  }
}

exports.JNIEnvInterceptorARM64 = s;

},{"../jni_env_interceptor":14}],12:[function(require,module,exports){
"use strict";

var t = this && this.__importDefault || function(t) {
  return t && t.__esModule ? t : {
    default: t
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JavaVM = void 0;

const e = t(require("../data/java_vm.json"));

class s {
  constructor() {
    this._methods = e.default;
  }
  get methods() {
    return this._methods;
  }
  static getInstance() {
    return void 0 === s.instance && (s.instance = new s), s.instance;
  }
}

exports.JavaVM = s;

},{"../data/java_vm.json":5}],13:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JavaVMInterceptor = void 0;

const e = require("./java_vm"), t = require("../utils/types"), a = require("../utils/config"), r = 0, n = 0, c = 1;

class s {
  constructor(e, t, a, r) {
    this.references = e, this.threads = t, this.jniEnvInterceptor = a, this.callbackManager = r, 
    this.shadowJavaVM = NULL;
  }
  isInitialised() {
    return !this.shadowJavaVM.isNull();
  }
  get() {
    return this.shadowJavaVM;
  }
  create() {
    const e = this.threads.getJavaVM(), t = Memory.alloc(8 * Process.pointerSize);
    this.references.add(t);
    const a = Memory.alloc(Process.pointerSize);
    a.writePointer(t);
    for (let a = 3; a < 8; a++) {
      const r = a * Process.pointerSize, n = e.readPointer().add(r).readPointer(), c = this.createJavaVMIntercept(a, n), s = this.jniEnvInterceptor.createStubFunction();
      this.references.add(s), Interceptor.replace(s, c), t.add(r).writePointer(s);
    }
    return this.shadowJavaVM = a, a;
  }
  createJavaVMIntercept(r, n) {
    const c = this, s = e.JavaVM.getInstance().methods[r], i = a.Config.getInstance(), o = s.args.map((e => t.Types.convertNativeJTypeToFridaType(e))), d = t.Types.convertNativeJTypeToFridaType(s.ret), h = new NativeFunction(n, d, o), l = new NativeCallback((function() {
      const e = this.threadId, t = c.threads.getJavaVM();
      let a = [].slice.call(arguments), r = NULL;
      a[0] = t;
      const o = {
        methodDef: s,
        jniAddress: n,
        threadId: e
      };
      "accurate" === i.backtrace ? o.backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE) : "fuzzy" === i.backtrace && (o.backtrace = Thread.backtrace(this.context, Backtracer.FUZZY)), 
      c.callbackManager.doBeforeCallback(s.name, o, a);
      let d = h.apply(null, a);
      return d = c.callbackManager.doAfterCallback(s.name, o, d), "GetEnv" !== s.name && "AttachCurrentThread" !== s.name && "AttachCurrentThreadAsDaemon" !== s.name || (0 === d && c.threads.setJNIEnv(e, a[1].readPointer()), 
      r = c.jniEnvInterceptor.isInitialised() ? c.jniEnvInterceptor.get() : c.jniEnvInterceptor.create(), 
      a[1].writePointer(r)), d;
    }), d, o);
    return this.references.add(l), l;
  }
}

exports.JavaVMInterceptor = s;

},{"../utils/config":19,"../utils/types":23,"./java_vm":12}],14:[function(require,module,exports){
"use strict";

var e = this && this.__importDefault || function(e) {
  return e && e.__esModule ? e : {
    default: e
  };
};

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNIEnvInterceptor = void 0;

const t = e(require("../data/jni_env.json")), a = require("../utils/types"), r = require("../utils/java_method"), s = require("../utils/config"), n = 0, i = -1, c = 0, o = 0;

class d {
  constructor(e, t, a) {
    this.references = e, this.threads = t, this.callbackManager = a, this.javaVMInterceptor = null, 
    this.shadowJNIEnv = NULL, this.methods = new Map, this.fastMethodLookup = new Map, 
    this.vaArgsBacktraces = new Map;
  }
  isInitialised() {
    return !this.shadowJNIEnv.equals(NULL);
  }
  get() {
    return this.shadowJNIEnv;
  }
  create() {
    const e = Process.getCurrentThreadId(), a = this.threads.getJNIEnv(e), r = Memory.alloc(232 * Process.pointerSize);
    this.references.add(r);
    const s = Memory.alloc(Process.pointerSize);
    s.writePointer(r), this.references.add(s);
    for (let e = 4; e < 232; e++) {
      const s = t.default[e], n = e * Process.pointerSize, i = a.readPointer().add(n).readPointer();
      if ("..." === s.args[s.args.length - 1]) {
        const t = this.createJNIVarArgIntercept(e, i), a = this.createStubFunction();
        this.references.add(a), Interceptor.replace(a, t), r.add(n).writePointer(a);
      } else {
        const t = this.createJNIIntercept(e, i), a = this.createStubFunction();
        this.references.add(a), Interceptor.replace(a, t), r.add(n).writePointer(a);
      }
    }
    return this.shadowJNIEnv = s, s;
  }
  setJavaVMInterceptor(e) {
    this.javaVMInterceptor = e;
  }
  createStubFunction() {
    return new NativeCallback((() => {}), "void", []);
  }
  createJNIVarArgIntercept(e, a) {
    const r = this, n = t.default[e], i = Memory.alloc(Process.pageSize), c = Memory.alloc(Process.pageSize);
    this.references.add(i), this.references.add(c);
    const o = this.createJNIVarArgInitialCallback(n, a);
    this.references.add(o), r.buildVaArgParserShellcode(i, c, o);
    const d = s.Config.getInstance();
    return Interceptor.attach(i, (function() {
      let e = Backtracer.ACCURATE;
      "fuzzy" === d.backtrace && (e = d.backtrace), r.vaArgsBacktraces.set(this.threadId, Thread.backtrace(this.context, e));
    })), i;
  }
  addJavaArgsForJNIIntercept(e, t) {
    let r = 2;
    e.name.includes("Nonvirtual") && (r = 3);
    const s = e.args.slice(-1)[0];
    if (![ "va_list", "jvalue*" ].includes(s)) return t.slice(0);
    const n = t.slice(0), i = t[r];
    if (!this.methods.has(i.toString())) return send({
      type: "error",
      message: 'Failed to find corresponding method ID for method "' + e.name + '" call.'
    }), t.slice(0);
    const c = this.methods.get(i.toString()), o = c.nativeParams, d = t.slice(-1)[0];
    "va_list" === s && this.setUpVaListArgExtract(d);
    for (let e = 0; e < o.length; e++) {
      const t = a.Types.convertNativeJTypeToFridaType(o[e]);
      let r;
      if ("va_list" === s) {
        const a = this.extractVaListArgValue(c, e);
        r = this.readValue(a, t, !0);
      } else r = this.readValue(d.add(8 * e), t);
      n.push(r);
    }
    return "va_list" === s && this.resetVaListArgExtract(), n;
  }
  handleGetMethodResult(e, t) {
    const a = e[3].readCString();
    if (null !== a) {
      const e = new r.JavaMethod(a);
      this.methods.set(t.toString(), e);
    }
  }
  handleGetJavaVM(e, t) {
    if (null !== this.javaVMInterceptor) {
      const a = 1;
      if (t === 0) {
        const t = e[a];
        let r;
        this.threads.setJavaVM(t.readPointer()), r = this.javaVMInterceptor.isInitialised() ? this.javaVMInterceptor.get() : this.javaVMInterceptor.create(), 
        t.writePointer(r);
      }
    }
  }
  handleRegisterNatives(e) {
    const t = this, a = e[2], r = e[3];
    for (let e = 0; e < 3 * r; e += 3) {
      const r = a, n = r.add(e * Process.pointerSize).readPointer().readCString(), i = 1, c = r.add((e + i) * Process.pointerSize).readPointer().readCString(), o = 2, d = r.add((e + o) * Process.pointerSize).readPointer();
      null !== n && null !== c && Interceptor.attach(d, {
        onEnter(e) {
          const a = n + c, r = s.Config.getInstance();
          if (r.includeExport.length > 0) {
            const e = r.includeExport.filter((e => a.includes(e)));
            if (0 === e.length) return;
          }
          if (r.excludeExport.length > 0) {
            if (r.excludeExport.filter((e => a.includes(e))).length > 0) return;
          }
          t.threads.hasJNIEnv(this.threadId) || t.threads.setJNIEnv(this.threadId, e[0]), 
          e[0] = t.shadowJNIEnv;
        }
      });
    }
  }
  handleJNIInterceptResult(e, t, a) {
    const r = e.name;
    [ "GetMethodID", "GetStaticMethodID" ].includes(r) ? this.handleGetMethodResult(t, a) : "GetJavaVM" === e.name ? this.handleGetJavaVM(t, a) : "RegisterNatives" === e.name && this.handleRegisterNatives(t);
  }
  createJNIIntercept(e, r) {
    const n = this, i = t.default[e], c = s.Config.getInstance(), o = i.args.map((e => a.Types.convertNativeJTypeToFridaType(e))), d = a.Types.convertNativeJTypeToFridaType(i.ret), l = new NativeFunction(r, d, o), h = new NativeCallback((function() {
      const e = this.threadId, t = n.threads.getJNIEnv(e), a = [].slice.call(arguments);
      a[0] = t;
      const s = n.addJavaArgsForJNIIntercept(i, a), o = {
        jniAddress: r,
        threadId: e,
        methodDef: i
      };
      if ("accurate" === c.backtrace ? o.backtrace = Thread.backtrace(this.context, Backtracer.ACCURATE) : "fuzzy" === c.backtrace && (o.backtrace = Thread.backtrace(this.context, Backtracer.FUZZY)), 
      a.length !== s.length) {
        const e = a[2].toString();
        o.javaMethod = n.methods.get(e);
      }
      n.callbackManager.doBeforeCallback(i.name, o, s);
      let d = l.apply(null, a);
      return d = n.callbackManager.doAfterCallback(i.name, o, d), n.handleJNIInterceptResult(i, a, d), 
      d;
    }), d, o);
    return this.references.add(h), h;
  }
  createJNIVarArgMainCallback(e, t, a, r, s) {
    const n = this, i = new NativeCallback((function() {
      const r = 2, i = this.threadId, c = [].slice.call(arguments), o = n.threads.getJNIEnv(i), d = c[r].toString(), l = n.methods.get(d);
      c[0] = o;
      const h = {
        backtrace: n.vaArgsBacktraces.get(this.threadId),
        jniAddress: t,
        threadId: i,
        methodDef: e,
        javaMethod: l
      };
      n.callbackManager.doBeforeCallback(e.name, h, c);
      let u = new NativeFunction(t, s, a).apply(null, c);
      return u = n.callbackManager.doAfterCallback(e.name, h, u), n.vaArgsBacktraces.delete(this.threadId), 
      u;
    }), s, r);
    return i;
  }
  createJNIVarArgInitialCallback(e, t) {
    const r = this, s = new NativeCallback((function() {
      const s = 2, n = arguments[s].toString(), i = r.methods.get(n);
      if (r.fastMethodLookup.has(n)) return r.fastMethodLookup.get(n);
      const c = e.args.slice(0, -1).map((e => a.Types.convertNativeJTypeToFridaType(e))), o = c.slice(0);
      c.push("..."), i.fridaParams.forEach((e => {
        o.push("float" === e ? "double" : e), c.push(e);
      }));
      const d = a.Types.convertNativeJTypeToFridaType(e.ret), l = r.createJNIVarArgMainCallback(e, t, c, o, d);
      return r.references.add(l), r.fastMethodLookup.set(n, l), l;
    }), "pointer", [ "pointer", "pointer", "pointer" ]);
    return s;
  }
  readValue(e, t, a) {
    let r = NULL;
    return "char" === t ? r = e.readS8() : "int16" === t ? r = e.readS16() : "uint16" === t ? r = e.readU16() : "int" === t ? r = e.readS32() : "int64" === t ? r = e.readS64() : "float" === t ? r = !0 === a ? e.readDouble() : e.readFloat() : "double" === t ? r = e.readDouble() : "pointer" === t && (r = e.readPointer()), 
    r;
  }
}

exports.JNIEnvInterceptor = d;

},{"../data/jni_env.json":6,"../utils/config":19,"../utils/java_method":21,"../utils/types":23}],15:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNIMethod = void 0;

class e {
  constructor(e, t, s) {
    this.name = e, this.args = t, this.ret = s;
  }
}

exports.JNIMethod = e;

},{}],16:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNIThreadManager = void 0;

class t {
  constructor() {
    this.threads = {}, this.shadowJavaVM = NULL;
  }
  getJavaVM() {
    return this.shadowJavaVM;
  }
  hasJavaVM() {
    return !this.shadowJavaVM.isNull();
  }
  setJavaVM(t) {
    this.shadowJavaVM = t;
  }
  getJNIEnv(t) {
    return void 0 !== this.threads[t] ? this.threads[t] : NULL;
  }
  hasJNIEnv(t) {
    return !this.getJNIEnv(t).isNull();
  }
  setJNIEnv(t, e) {
    this.createEntry(t, e);
  }
  needsJNIEnvUpdate(t, e) {
    const s = this.getEntry(t);
    return void 0 === s || !s.equals(e);
  }
  createEntry(t, e) {
    this.threads[t] = e;
  }
  getEntry(t) {
    return this.threads[t];
  }
}

exports.JNIThreadManager = t;

},{}],17:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNIEnvInterceptorX64 = void 0;

const t = require("../jni_env_interceptor");

class e extends t.JNIEnvInterceptor {
  constructor(t, e, r) {
    super(t, e, r), this.grOffset = 0, this.grOffsetStart = 0, this.fpOffset = 0, this.fpOffsetStart = 0, 
    this.overflowPtr = NULL, this.dataPtr = NULL;
  }
  buildVaArgParserShellcode(t, e, r) {
    Memory.patchCode(t, Process.pageSize, (s => {
      const i = new X86Writer(s, {
        pc: t
      }), o = [ "rdi", "rsi", "rdx", "rcx", "r8", "r9", "rax", "rbx", "r10", "r11", "r12", "r13", "r14", "r15", "xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7" ];
      let a = 0, f = 0;
      for (let t = 0; t < o.length; t++) i.putMovNearPtrReg(e.add(a), "rdi"), a += Process.pointerSize, 
      t < o.length - 1 && (o[t + 1].includes("xmm") ? (i.putU8(102), i.putU8(72), i.putU8(15), 
      i.putU8(126), i.putU8(199 + 8 * f), f++) : i.putMovRegReg("rdi", o[t + 1]));
      f--, i.putPopReg("rdi"), i.putMovNearPtrReg(e.add(a), "rdi"), a += Process.pointerSize, 
      i.putCallAddress(r), i.putMovNearPtrReg(e.add(a), "rax"), a += Process.pointerSize;
      let d = a - 2 * Process.pointerSize;
      for (let t = o.length - 1; t >= 0; t--) d = t * Process.pointerSize, i.putMovRegNearPtr("rdi", e.add(d)), 
      t > 0 && (o[t].includes("xmm") ? (i.putU8(102), i.putU8(72), i.putU8(15), i.putU8(110), 
      i.putU8(199 + 8 * f), f--) : i.putMovRegReg(o[t], "rdi"));
      i.putMovNearPtrReg(e.add(a), "rdi");
      const p = a;
      a += Process.pointerSize;
      const n = p - Process.pointerSize;
      i.putMovRegNearPtr("rdi", e.add(n)), i.putMovNearPtrReg(e.add(a), "r13");
      const P = a;
      i.putMovRegReg("r13", "rdi"), i.putMovRegNearPtr("rdi", e.add(p)), i.putCallReg("r13"), 
      i.putMovRegNearPtr("r13", e.add(P));
      const c = n - Process.pointerSize;
      i.putJmpNearPtr(e.add(c)), i.flush();
    }));
  }
  setUpVaListArgExtract(t) {
    this.grOffset = t.readU32(), this.grOffsetStart = this.grOffset, this.fpOffset = t.add(4).readU32(), 
    this.fpOffsetStart = this.fpOffset, this.overflowPtr = t.add(Process.pointerSize).readPointer(), 
    this.dataPtr = t.add(2 * Process.pointerSize).readPointer();
  }
  extractVaListArgValue(t, e) {
    let r = NULL;
    if ("float" === t.fridaParams[e] || "double" === t.fridaParams[e]) {
      if ((this.fpOffset - this.fpOffsetStart) / Process.pointerSize < 14) r = this.dataPtr.add(this.fpOffset), 
      this.fpOffset += 2 * Process.pointerSize; else {
        const s = t.fridaParams.length - e - 1;
        r = this.overflowPtr.add(s * Process.pointerSize);
      }
    } else {
      if ((this.grOffset - this.grOffsetStart) / Process.pointerSize < 2) r = this.dataPtr.add(this.grOffset), 
      this.grOffset += Process.pointerSize; else {
        const s = t.fridaParams.length - e - 1;
        r = this.overflowPtr.add(s * Process.pointerSize);
      }
    }
    return r;
  }
  resetVaListArgExtract() {
    this.grOffset = 0, this.grOffsetStart = 0, this.fpOffset = 0, this.fpOffsetStart = 0, 
    this.overflowPtr = NULL, this.dataPtr = NULL;
  }
}

exports.JNIEnvInterceptorX64 = e;

},{"../jni_env_interceptor":14}],18:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JNIEnvInterceptorX86 = void 0;

const e = require("../jni_env_interceptor"), t = require("../../utils/types");

class s extends e.JNIEnvInterceptor {
  constructor(e, t, s) {
    super(e, t, s), this.vaList = NULL, this.vaListOffset = 0;
  }
  buildVaArgParserShellcode(e, t, s) {
    e.add(1024).writePointer(s), Memory.patchCode(e, Process.pageSize, (t => {
      const r = new X86Writer(t, {
        pc: e
      }), i = 1024 + Process.pointerSize;
      r.putPopReg("eax"), r.putMovNearPtrReg(e.add(i + Process.pointerSize), "eax"), r.putCallAddress(s), 
      r.putCallReg("eax"), r.putJmpNearPtr(e.add(i + Process.pointerSize)), r.flush();
    }));
  }
  setUpVaListArgExtract(e) {
    this.vaList = e, this.vaListOffset = 0;
  }
  extractVaListArgValue(e, s) {
    let r = this.vaList.add(this.vaListOffset);
    return this.vaListOffset += t.Types.sizeOf(e.fridaParams[s]), r;
  }
  resetVaListArgExtract() {
    this.vaList = NULL, this.vaListOffset = 0;
  }
}

exports.JNIEnvInterceptorX86 = s;

},{"../../utils/types":23,"../jni_env_interceptor":14}],19:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.Config = void 0;

const e = require("./config_builder");

class t {
  constructor(e) {
    this._libraries = e.libraries, this._backtrace = e.backtrace, this._includeExport = e.includeExports, 
    this._excludeExport = e.excludeExports, this._env = e.env, this._vm = e.vm, this._hostInitialised = !1;
  }
  get libraries() {
    return this._libraries;
  }
  get backtrace() {
    return this._backtrace;
  }
  get includeExport() {
    return this._includeExport;
  }
  get excludeExport() {
    return this._excludeExport;
  }
  get env() {
    return this._env;
  }
  get vm() {
    return this._vm;
  }
  static initialised() {
    return void 0 !== t.instance && t.instance._hostInitialised;
  }
  static getInstance(i) {
    return void 0 !== i ? (t.instance = new t(i), t.instance._hostInitialised = !0) : void 0 === t.instance && (t.instance = new t(new e.ConfigBuilder)), 
    t.instance;
  }
}

exports.Config = t;

},{"./config_builder":20}],20:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.ConfigBuilder = void 0;

const e = require("./config");

class t {
  constructor() {
    this._libraries = [ "*" ], this._backtrace = "accurate", this._includeExports = [], 
    this._excludeExports = [], this._env = !0, this._vm = !0;
  }
  set libraries(e) {
    this._libraries = e;
  }
  get libraries() {
    return this._libraries;
  }
  set backtrace(e) {
    if (![ "fuzzy", "accurate", "none" ].includes(e)) throw new Error("Backtracer value must be one of the following, [fuzzy, accurate, none].");
    this._backtrace = e;
  }
  get backtrace() {
    return this._backtrace;
  }
  set includeExports(e) {
    this._includeExports = e;
  }
  get includeExports() {
    return this._includeExports;
  }
  set excludeExports(e) {
    this._excludeExports = e;
  }
  get excludeExports() {
    return this._excludeExports;
  }
  set env(e) {
    this._env = e;
  }
  get env() {
    return this._env;
  }
  set vm(e) {
    this._vm = e;
  }
  get vm() {
    return this._vm;
  }
  build() {
    return e.Config.getInstance(this);
  }
}

exports.ConfigBuilder = t;

},{"./config":19}],21:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.JavaMethod = void 0;

const e = require("./types"), t = 1;

class r {
  constructor(e) {
    const t = [ "B", "S", "I", "J", "F", "D", "C", "Z", "V" ];
    let r = !1, s = !1;
    const a = [];
    let n = "unknown";
    for (var o = 0; o < e.length; o++) {
      if ("(" === e.charAt(o)) continue;
      if (")" === e.charAt(o)) {
        s = !0;
        continue;
      }
      if ("[" === e.charAt(o)) {
        r = !0;
        continue;
      }
      let c = "unknown";
      if (t.includes(e.charAt(o))) c = e.charAt(o); else if ("L" === e.charAt(o)) {
        var i = e.indexOf(";", o) + 1;
        c = e.substring(o, i), o = i - 1;
      }
      r && (c = "[" + c), s ? n = c : a.push(c), r = !1;
    }
    this._ = e, this._params = a, this._ret = n;
  }
  get params() {
    return this._params;
  }
  get nativeParams() {
    const t = [];
    return this._params.forEach((r => {
      const s = e.Types.convertJTypeToNativeJType(r);
      t.push(s);
    })), t;
  }
  get fridaParams() {
    const t = [];
    return this._params.forEach((r => {
      const s = e.Types.convertJTypeToNativeJType(r), a = e.Types.convertNativeJTypeToFridaType(s);
      t.push(a);
    })), t;
  }
  get ret() {
    return this._ret;
  }
  get fridaRet() {
    const t = e.Types.convertJTypeToNativeJType(this._ret);
    return e.Types.convertNativeJTypeToFridaType(t);
  }
}

exports.JavaMethod = r;

},{"./types":23}],22:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.ReferenceManager = void 0;

class e {
  constructor() {
    this.references = new Map;
  }
  add(e) {
    this.references.set(e.toString(), e);
  }
  release(e) {
    this.references.has(e.toString()) && this.references.delete(e.toString());
  }
}

exports.ReferenceManager = e;

},{}],23:[function(require,module,exports){
"use strict";

Object.defineProperty(exports, "__esModule", {
  value: !0
}), exports.Types = void 0;

const t = 1, e = 8, j = 1, o = {
  isComplexObjectType: t => [ "jobject", "jclass", "jweak" ].includes(t),
  sizeOf: t => "double" === t || "float" === t || "int64" === t ? 8 : "char" === t ? 1 : Process.pointerSize,
  convertNativeJTypeToFridaType: t => t.endsWith("*") || "va_list" === t || "jmethodID" === t || "jfieldID" === t ? "pointer" : "va_list" === t ? "va_list" : ("jweak" === t && (t = "jobject"), 
  "jthrowable" === t && (t = "jobject"), t.includes("Array") && (t = "jarray"), "jarray" === t && (t = "jobject"), 
  "jstring" === t && (t = "jobject"), "jclass" === t && (t = "jobject"), "jobject" === t ? "pointer" : ("jsize" === t && (t = "jint"), 
  "jdouble" === t ? "double" : "jfloat" === t ? "float" : "jchar" === t ? "uint16" : "jboolean" === t ? "char" : "jlong" === t ? "int64" : "jint" === t ? "int" : "jshort" === t ? "int16" : "jbyte" === t ? "char" : t)),
  convertJTypeToNativeJType(t) {
    let e = "", j = !1;
    return t.startsWith("[") && (j = !0, t = t.substring(1)), "B" === t ? e += "jbyte" : "S" === t ? e += "jshort" : "I" === t ? e += "jint" : "J" === t ? e += "jlong" : "F" === t ? e += "jfloat" : "D" === t ? e += "jdouble" : "C" === t ? e += "jchar" : "Z" === t ? e += "jboolean" : t.startsWith("L") && (e += "Ljava/lang/String;" === t ? "jstring" : "Ljava/lang/Class;" === t ? "jclass" : "jobject"), 
    j && ("jstring" === e && (e = "jobject"), e += "Array"), e;
  }
};

exports.Types = o;

},{}]},{},[1])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9icm93c2VyLXBhY2svX3ByZWx1ZGUuanMiLCJqbml0cmFjZS9zcmMvbWFpbi50cyIsImpuaXRyYWNlL3NyYy90cmFuc3BvcnQvZGF0YV90cmFuc3BvcnQudHMiLCJqbml0cmFjZS9zcmMvdXRpbHMvbWV0aG9kX2RhdGEudHMiLCJqbml0cmFjZS9zcmMvdXRpbHMvdHlwZXMudHMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3QvZGF0YS9qYXZhX3ZtLmpzb24iLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3QvZGF0YS9qbmlfZW52Lmpzb24iLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3QvZW5naW5lLmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L2luZGV4LmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L2ludGVybmFsL2puaV9jYWxsYmFja19tYW5hZ2VyLmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L2puaS9hcm0vam5pX2Vudl9pbnRlcmNlcHRvcl9hcm0uanMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3Qvam5pL2FybTY0L2puaV9lbnZfaW50ZXJjZXB0b3JfYXJtNjQuanMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3Qvam5pL2phdmFfdm0uanMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3Qvam5pL2phdmFfdm1faW50ZXJjZXB0b3IuanMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3Qvam5pL2puaV9lbnZfaW50ZXJjZXB0b3IuanMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3Qvam5pL2puaV9tZXRob2QuanMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3Qvam5pL2puaV90aHJlYWRfbWFuYWdlci5qcyIsIm5vZGVfbW9kdWxlcy9qbml0cmFjZS1lbmdpbmUvZGlzdC9qbmkveDY0L2puaV9lbnZfaW50ZXJjZXB0b3JfeDY0LmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L2puaS94ODYvam5pX2Vudl9pbnRlcmNlcHRvcl94ODYuanMiLCJub2RlX21vZHVsZXMvam5pdHJhY2UtZW5naW5lL2Rpc3QvdXRpbHMvY29uZmlnLmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L3V0aWxzL2NvbmZpZ19idWlsZGVyLmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L3V0aWxzL2phdmFfbWV0aG9kLmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L3V0aWxzL3JlZmVyZW5jZV9tYW5hZ2VyLmpzIiwibm9kZV9tb2R1bGVzL2puaXRyYWNlLWVuZ2luZS9kaXN0L3V0aWxzL3R5cGVzLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBOzs7Ozs7O0FDQUEsTUFBQSxJQUFBLFFBQUEsb0JBQ0EsSUFBQSxRQUFBLG9CQUdBLElBQUEsUUFBQSxvQkFDQSxJQUFBLFFBQUEsb0JBQ0EsSUFBQSxRQUFBLHdCQUNBLElBQUEsUUFBQSwrQkFFTSxLQUFhLEdBQ2IsSUFBWSxJQUFJLEVBQUE7O0FBQ3RCLElBQUksSUFBd0I7O0FBRTVCLEVBQUEsa0JBQWtCLFlBQVk7RUFDMUIsU0FBVTtJQUVOLEtBQW9CLEVBQUEsT0FBTyxlQUFlO01BRTNCLEtBQUssV0FBVztRQUN2QixNQUFNLElBQVUsSUFBSSxFQUFBO1FBR3BCLEVBQVEsWUFBWSxFQUFRLFFBQVEsV0FDcEMsRUFBUSxZQUFZLEVBQVEsUUFBUSxXQUNwQyxFQUFRLGlCQUFpQixFQUFRLFFBQVE7UUFDekMsRUFBUSxpQkFBaUIsRUFBUSxRQUFRLGdCQUN6QyxFQUFRLE1BQU0sRUFBUSxRQUFRLEtBQzlCLEVBQVEsS0FBSyxFQUFRLFFBQVE7UUFFN0IsSUFBUyxFQUFRLFNBRWpCLEVB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QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7Ozs7Ozs7O0FDdFJBLE1BQU07RUFXRixZQUNJLEdBQ0EsR0FDQSxHQUNBO0lBRUEsS0FBSyxVQUFVLEdBQ2YsS0FBSyxXQUFXLEdBQ2hCLEtBQUssUUFBUSxHQUNiLEtBQUssT0FBTyxHQUVSLEtBQUssZ0JBRE8sTUFBWixJQUNnQixLQUVBLEVBQVE7QUFFaEM7RUFFVztJQUNQLE9BQU8sS0FBSztBQUNoQjtFQUVXO0lBQ1AsT0FBTyxLQUFLO0FBQ2hCO0VBRVc7SUFDUCxPQUFPLEtBQUs7QUFDaEI7RUFFTyxZQUFhO0lBQ2hCLE9BQU8sS0FBSyxNQUFNO0FBQ3RCO0VBRU8sWUFBYTtJQUNoQixPQUFPLEtBQUssTUFBTTtBQUN0QjtFQUVXO0lBQ1AsT0FBTyxLQUFLO0FBQ2hCO0VBRVc7SUFDUCxPQUFPLEtBQUs7QUFDaEI7OztBQUdLLFFBQUE7OztBQzdEVDtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNyQkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUMxREE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQzFyRUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQ2pHQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNoR0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ3RDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDeERBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDbkVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUM1QkE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUNwREE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ3pMQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQ2JBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUN6Q0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDckVBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDbENBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FDMUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUN4REE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7O0FDNURBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQ3BCQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSIsImZpbGUiOiJnZW5lcmF0ZWQuanMiLCJzb3VyY2VSb290IjoiIn0=
