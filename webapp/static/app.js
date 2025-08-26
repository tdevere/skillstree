let skillTree = null
let progress = {}

function toast(msg, timeout=2500){
  const t = document.getElementById('toast')
  t.textContent = msg
  t.style.display = 'block'
  setTimeout(()=>t.style.display='none', timeout)
}

async function loadProgress(){
  try{
    const r = await fetch('/api/progress')
    progress = await r.json()
  }catch(e){progress={}}
}

async function saveProgress(){
  try{
    const r = await fetch('/api/progress',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(progress)})
    const j = await r.json()
    document.getElementById('saveStatus').textContent = j.status||'saved'
    toast('Progress saved')
  }catch(e){toast('Save failed')}
}

function makeRankControl(nodeId, rankId, rankObj){
  const wrapper = document.createElement('div')
  wrapper.className = 'rank'
  const key = `${nodeId}#${rankId}`
  const checked = progress[key]||false
  wrapper.innerHTML = `<label><div>Rank ${rankId}</div><input type=checkbox ${checked? 'checked':''} /> <div class='cap'>${rankObj.capabilities}</div></label>`
  const cb = wrapper.querySelector('input')
  cb.addEventListener('change', e=>{
    progress[key] = e.target.checked
    saveProgress()
  })
  return wrapper
}

async function render(){
  const res = await fetch('/api/skill_tree')
  skillTree = await res.json()
  await loadProgress()
  const content = document.getElementById('content')
  content.innerHTML = ''
  const nodes = skillTree.nodes || {}
  for(const id of Object.keys(nodes)){
    const node = nodes[id]
    const card = document.createElement('section')
    card.className = 'card'
    card.innerHTML = `<h2>${id} — ${node.title}</h2><p>${node.path}</p>`
    const ranks = node.ranks || {}
    const ranksDiv = document.createElement('div')
    ranksDiv.className = 'ranks'
    for(const r of Object.keys(ranks)){
      const ctrl = makeRankControl(id, r, ranks[r])
      ranksDiv.appendChild(ctrl)
    }
    card.appendChild(ranksDiv)
    content.appendChild(card)
  }
}

document.getElementById('refreshBtn').addEventListener('click', ()=>{render(); toast('Refreshed')})

render()
