import React from 'react';
import {AbsoluteFill,Composition,Easing,Img,Sequence,staticFile,interpolate,useCurrentFrame} from 'remotion';
import {Video} from '@remotion/media';
import captions from './captions.json';

const green='#4ade80',white='#f7f7f3',mute='#b8b8b8';
const clamp={extrapolateLeft:'clamp' as const,extrapolateRight:'clamp' as const};
const TOP_H=1070;               // metade de cima: rosto do Leo, FIXO, nunca coberto
const BAND_H=1920-TOP_H;        // metade de baixo: todo o apoio mora aqui

const Reveal:React.FC<React.PropsWithChildren<{delay?:number}>>=({children,delay=0})=>{
  const f=useCurrentFrame();
  const p=interpolate(f,[delay,delay+18],[0,1],{...clamp,easing:Easing.bezier(.16,1,.3,1)});
  return <div style={{opacity:p,clipPath:`inset(0 ${(1-p)*100}% 0 0)`,transform:`translateY(${(1-p)*24}px)`}}>{children}</div>;
};

// pontos aparecendo UM POR VEZ (revelacao progressiva, empilhados)
const Bullets:React.FC<{items:string[];delay:number}>=({items,delay})=>(
  <div style={{display:'flex',flexDirection:'column',gap:22,marginTop:46}}>
    {items.map((it,i)=><Reveal key={i} delay={delay+i*14}>
      <div style={{display:'flex',alignItems:'center',gap:20}}>
        <div style={{width:26,height:26,flexShrink:0,border:`2px solid ${green}`,borderRadius:6,background:'rgba(74,222,128,.12)'}}/>
        <div style={{fontSize:42,fontWeight:600,color:white,lineHeight:1.15}}>{it}</div>
      </div>
    </Reveal>)}
  </div>
);

// cabecalho da faixa (eyebrow + titulo) — comum a slide e a tela
const Eyebrow:React.FC<{eyebrow:string}>=({eyebrow})=>(
  <Reveal><div style={{display:'flex',alignItems:'center',gap:16}}><div style={{width:40,height:6,background:green,borderRadius:3}}/><div style={{fontSize:28,fontWeight:800,color:green,letterSpacing:3,textTransform:'uppercase'}}>{eyebrow}</div></div></Reveal>
);
const Title:React.FC<{line1:string;accent:string;delay?:number}>=({line1,accent,delay=12})=>(
  <Reveal delay={delay}><div style={{fontSize:88,lineHeight:.98,fontWeight:900,letterSpacing:-3,color:white,marginTop:36}}>{line1}<br/><span style={{color:green}}>{accent}</span></div></Reveal>
);

// SLIDE de texto (metade de baixo) — pontos um a um
const Lower:React.FC<{eyebrow:string;line1:string;accent:string;body?:string;dur:number}>=({eyebrow,line1,accent,body,dur})=>{
  const f=useCurrentFrame();
  const items=body?(body.includes('→')?body.split('→'):body.includes('·')?body.split('·'):[]).map(s=>s.trim()).filter(Boolean):[];
  const bar=interpolate(f,[0,dur],[0,1],clamp);
  return <AbsoluteFill style={{top:TOP_H,height:BAND_H,background:'#000',padding:'56px 84px 96px',fontFamily:'Inter',display:'flex',flexDirection:'column',justifyContent:'center'}}>
    <Eyebrow eyebrow={eyebrow}/>
    <Title line1={line1} accent={accent}/>
    {items.length>0
      ? <Bullets items={items} delay={34}/>
      : body&&<Reveal delay={34}><div style={{fontSize:40,lineHeight:1.4,fontWeight:400,color:mute,marginTop:48,maxWidth:912}}>{body}</div></Reveal>}
    <div style={{position:'absolute',left:84,right:84,bottom:52,height:4,background:'rgba(255,255,255,.12)',borderRadius:2}}>
      <div style={{height:'100%',width:`${bar*100}%`,background:green,borderRadius:2}}/>
    </div>
  </AbsoluteFill>;
};

// TELA (video/print) na metade de baixo: o slide entra 1s, depois a tela toma a faixa (o slide "sai")
const LowerScreen:React.FC<{eyebrow:string;line1:string;accent:string;kind:'video'|'img';src:string;dur:number}>=({eyebrow,line1,accent,kind,src,dur})=>{
  const f=useCurrentFrame();
  const swap=42;                                   // frames de slide antes da tela assumir
  const slideOut=interpolate(f,[swap,swap+16],[1,0],clamp);        // slide sai
  const screenIn=interpolate(f,[swap+6,swap+28],[0,1],clamp);      // tela entra
  const bar=interpolate(f,[0,dur],[0,1],clamp);
  return <AbsoluteFill style={{top:TOP_H,height:BAND_H,background:'#000',fontFamily:'Inter',overflow:'hidden'}}>
    {/* slide breve (sai quando a tela entra) */}
    <div style={{position:'absolute',inset:0,padding:'56px 84px',display:'flex',flexDirection:'column',justifyContent:'center',opacity:slideOut}}>
      <Eyebrow eyebrow={eyebrow}/>
      <Title line1={line1} accent={accent}/>
    </div>
    {/* a TELA ocupando a faixa de baixo */}
    <div style={{position:'absolute',inset:0,display:'flex',flexDirection:'column',opacity:screenIn}}>
      <div style={{padding:'26px 84px 6px',display:'flex',alignItems:'center',gap:14}}>
        <div style={{width:34,height:6,background:green,borderRadius:3}}/>
        <div style={{fontSize:26,fontWeight:800,color:green,letterSpacing:3,textTransform:'uppercase'}}>{eyebrow}</div>
      </div>
      <div style={{flex:1,minHeight:0,display:'flex',alignItems:'center',justifyContent:'center',padding:'0 40px 40px'}}>
        {kind==='video'
          ? <Video src={staticFile(src)} loop style={{maxWidth:'100%',maxHeight:'100%',objectFit:'contain',borderRadius:14,border:'1px solid rgba(74,222,128,.25)'}}/>
          : <Img src={staticFile(src)} style={{maxWidth:'100%',maxHeight:'100%',objectFit:'contain',borderRadius:14,border:'1px solid rgba(74,222,128,.25)'}}/>}
      </div>
    </div>
    <div style={{position:'absolute',left:84,right:84,bottom:34,height:4,background:'rgba(255,255,255,.12)',borderRadius:2}}>
      <div style={{height:'100%',width:`${bar*100}%`,background:green,borderRadius:2}}/>
    </div>
  </AbsoluteFill>;
};

// legenda da fala, sempre SOBRE o rosto, logo acima da linha da metade
const Caption:React.FC=()=>{
  const f=useCurrentFrame();const ms=f/30*1000;
  const cur=(captions as any[]).find(c=>ms>=c.startMs&&ms<c.endMs);
  if(!cur)return null;
  return <div style={{position:'absolute',left:70,right:70,top:TOP_H-186,textAlign:'center',fontFamily:'Inter'}}>
    <span style={{display:'inline',boxDecorationBreak:'clone' as const,WebkitBoxDecorationBreak:'clone' as const,background:'rgba(0,0,0,.62)',color:white,fontSize:40,fontWeight:700,lineHeight:1.42,letterSpacing:-.5,padding:'6px 14px',borderRadius:4}}>{cur.text}</span>
  </div>;
};

const Director=()=> <AbsoluteFill style={{background:'#000'}}>
  {/* METADE DE CIMA: rosto LIMPO do Leo (clean_top.mp4), FIXO o video inteiro, nunca coberto */}
  <div style={{position:'absolute',top:0,left:0,width:1080,height:TOP_H,overflow:'hidden'}}>
    <Video src={staticFile('clean_top.mp4')} durationInFrames={1845} style={{position:'absolute',top:-700,left:-135,width:1350,height:2400}}/>
  </div>
  <Caption/>
  {/* METADE DE BAIXO: todo o apoio (slides com pontos um-a-um + telas), nunca invade o topo */}
  <Sequence from={0} durationInFrames={180}><Lower dur={180} eyebrow="Caso real" line1="O que um agente faz" accent="pela sua empresa?"/></Sequence>
  <Sequence from={180} durationInFrames={360}><Lower dur={360} eyebrow="Caso Augusto" line1="Uma operação de" accent="~ R$ 5 mi/ano" body="Educação online · Harmonização facial"/></Sequence>
  <Sequence from={540} durationInFrames={350}><Lower dur={350} eyebrow="Antes" line1="Duas semanas" accent="para cada volta" body="Copy · análise · web design · feedback · retrabalho"/></Sequence>
  <Sequence from={890} durationInFrames={350}><Lower dur={350} eyebrow="Agora" line1="Um áudio." accent="Página pronta." body="Outro áudio · 100% pronta no domínio"/></Sequence>
  <Sequence from={1240} durationInFrames={310}><LowerScreen dur={310} eyebrow="Interface" line1="Direto com o agente" accent="no Telegram." kind="video" src="telegram.mp4"/></Sequence>
  <Sequence from={1550} durationInFrames={295}><LowerScreen dur={295} eyebrow="Resultado" line1="Eficiência" accent="operacional." kind="img" src="ops.png"/></Sequence>
</AbsoluteFill>;

export const Root=()=> <Composition id="Director" component={Director} durationInFrames={1845} fps={30} width={1080} height={1920}/>;
