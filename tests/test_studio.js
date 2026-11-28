"use strict";
const fs=require("node:fs"),assert=require("node:assert/strict"),vm=require("node:vm"),path=require("node:path");
const root=path.join(__dirname,"..");
const html=fs.readFileSync(path.join(root,"codebase/studio.html"),"utf8");
const sandbox={module:{exports:{}}};
vm.runInNewContext(html.match(/<script id="logic">([\s\S]*?)<\/script>/)[1],sandbox);
const {validate}=sandbox.module.exports;
const fixture=JSON.parse(fs.readFileSync(path.join(root,"data/fixtures/script_response.json"),"utf8"));
const dataset=JSON.parse(fs.readFileSync(path.join(root,"data/lessons/oop_annotations.json"),"utf8"));
const codes=new Set(fixture.segments.flatMap(s=>s.slide_refs));
fixture.sources=dataset.lessons[0].segments.filter(s=>codes.has(s.code));
const cases=[
 ["valid multi-segment",()=>{},null],
 ["null root",()=>null,"SCHEMA"],
 ["null segments",p=>{p.segments=null},"SCHEMA"],
 ["null segment",p=>{p.segments[0]=null},"SCHEMA"],
 ["missing objective",p=>{p.learning_objectives=[]},"SCHEMA"],
 ["wrong field type",p=>{p.segments[0].teacher_script={}},"SCHEMA"],
 ["empty field",p=>{p.segments[0].assessment=" "},"SCHEMA"],
 ["missing warnings",p=>{delete p.warnings},"SCHEMA"],
 ["bad assumptions",p=>{p.assumptions=[42]},"SCHEMA"],
 ["auto approval",p=>{p.status="approved"},"STATUS"],
 ["approval metadata",p=>{p.approved_by="AI"},"STATUS"],
 ["wrong total",p=>{p.duration_minutes=61},"TIMELINE"],
 ["gap",p=>{p.segments[1].start_minute++},"TIMELINE"],
 ["fraction minutes",p=>{p.segments[0].duration_minutes=5.5},"TIMELINE"],
 ["invalid refs",p=>{p.segments[0].slide_refs=null},"REF"],
 ["unknown ref",p=>{p.segments[0].slide_refs=["missing"]},"REF"],
 ["out of scope source",p=>{p.sources.push({code:"X",text:"foreign"})},"REF"],
 ["duplicate source",p=>{p.sources.push(p.sources[0])},"REF"],
 ["html edit",p=>{p.segments[0].teacher_script="<script>alert(1)</script>"},"UNSAFE"],
 ["html title",p=>{p.lesson_title="<b>Title</b>"},"UNSAFE"],
 ["javascript URI",p=>{p.segments[0].fallback_strategy="javascript : alert(1)"},"UNSAFE"],
 ["long Vietnamese script",p=>{p.segments[0].teacher_script="Lời dẫn giảng viên.\n".repeat(500)} ,null],
 ["ordinary comparisons",p=>{p.segments[0].teacher_script="Nếu x < 1 hoặc x > 9 thì kiểm tra."},null],
];
for(const [name,mutate,error] of cases){
 const p=structuredClone(fixture);
 const changed=mutate(p);
 const errs=validate(changed===null?null:p,60,codes);
 if(error)assert.ok(errs.some(e=>e.includes("["+error+"]")),name+": "+errs.join(";"));
 else assert.equal(errs.length,0,name+": "+errs.join(";"));
 console.log("PASS "+name);
}
console.log(cases.length+" studio validation cases passed.");
