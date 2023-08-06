import React, { useCallback, useEffect, useMemo, useRef } from "react"

import { Streamlit } from "streamlit-component-lib"
import { useStreamlit } from "streamlit-component-lib-react-hooks"

import { VTKViewer, VTKViewerDrawer, VTKFloatingToolbar } from "pollination-viewer"

import { Layout } from "antd"

import './VTKStreamlit.css'

import isequal from "lodash.isequal"
import debounce from "lodash.debounce"

const HEIGHT = 640

const VTKStreamlit: React.FunctionComponent = () => {

  const renderData = useStreamlit()

  const viewerRef = useRef<any>(null)

  // state returned to streamlit
  const [viewerState, setViewerState] = React.useState<any>({})
  const viewerSceneRef = useRef<any[]>([])

  // stack of actions to dispatch via vtkjs
  const actionStackRef = useRef<any[]>([])

  // file to be loaded
  const [file, setFile] = React.useState<Uint8Array | undefined>(undefined)

  const handleScreenshot = useCallback((fileName='VTKJSStreamlit') => {
    if (!viewerRef.current) return
    viewerRef.current.handleScreenshot(fileName, false)
  }, [])

  useEffect(() => {
    if (renderData && renderData.args["subscribe"]) {
      Streamlit.setComponentValue(viewerState)
    } else if (viewerState.scene && viewerState.scene.length > 0) {
      const scene = viewerState.scene.map(({id}: {id: string}) => id)
      const ref = viewerSceneRef.current.map(({id}: {id: string}) => id)

      if (isequal(scene, ref)) return
      
      viewerSceneRef.current = [...viewerState.scene]

      Streamlit.setComponentValue({
        scene: viewerSceneRef.current
      })
    }
  }, [viewerState, renderData])

  // aggreate and dispatch actions on a debounced interval
  const dispatchActionStack = useCallback(() => {
    if (viewerRef.current && viewerRef.current.dispatch &&
      actionStackRef.current && actionStackRef.current.length > 0) {

      // handles screenshot as a special case
      const screenshotIndex = actionStackRef.current.findIndex(a => a.type === "streamlit-screenshot")
      if (screenshotIndex !== -1) {
        const screenshotName = renderData?.args && renderData.args['screenshot_name'] ? renderData.args['screenshot_name'] : undefined
        if (!screenshotName) {
          console.log(renderData?.args)
        }
        handleScreenshot(screenshotName)
      }

      // filters type === "strealit-screenshot", and actions with duplicate types
      // any action with ids [] will be dispatched
      const actions = [...actionStackRef.current].reverse()
        .filter((action, i, array) =>
          (action.type !== "streamlit-screenshot" &&
            typeof action.ids !== 'undefined') ||
          array.findIndex(a => a.type === action.type) === i
        )

      viewerRef.current.dispatch(actions)
      actionStackRef.current = []
    }
  }, [handleScreenshot, renderData])

  const debouncedDispatch = useCallback(debounce(dispatchActionStack, 250, { leading:true, maxWait: 750 }), [dispatchActionStack])

  useEffect(() => {
    if (renderData && typeof renderData.args["action_stack"] !== undefined
      && viewerRef.current && viewerRef.current.dispatch) {
      actionStackRef.current = [
        ...actionStackRef.current,
        ...renderData.args["action_stack"]
      ]
      if (actionStackRef.current.length > 0) {
        debouncedDispatch()
      }
    }
  }, [renderData, debouncedDispatch])

  useEffect(() => {
    if (renderData && renderData.args["content"]) {
      setFile(currFile => {
        if (!currFile) return renderData.args["content"]
        const equal = isequal(renderData.args["content"], currFile)
        return equal ? currFile : renderData.args["content"]
      })
    }
  }, [renderData])
  
  const loadFile = (file: Uint8Array) => {
    if (viewerRef.current && viewerRef.current.dispatch && viewerRef.current.loadFile) {

      if(renderData && renderData.args["clear"]) viewerRef.current.dispatch({ type: 'remove-all' }, true)

      const scene = viewerSceneRef.current
      if (!scene) return

      const config = scene.length > 0 ? scene : undefined

      viewerRef.current.loadFile(new Blob([file]), 'vtkjs', config)
    }
  }

  useEffect(() => {
    if (!file) return
    loadFile(file)
    // eslint-disable-next-line
  }, [file])

  useEffect(() => {
    if (!renderData) return
    
    if (typeof renderData.args["style"] !== 'undefined' && 
        renderData.args["style"].height && 
        renderData.args["style"].height.includes('px')) {
          Streamlit.setFrameHeight(parseInt(renderData.args["style"].height.replace('px', '')))
    } else {
      Streamlit.setFrameHeight(HEIGHT)
    }
  }, [renderData])

  const cssStyle = useMemo(() => {
    return renderData && typeof renderData.args["style"] !== 'undefined' ? 
      renderData.args["style"] : 
      { border: "1px solid #d0d7de", borderRadius: "2px", height: `${HEIGHT}px` }
  }, [renderData])

  const toolbar = renderData && typeof renderData.args["toolbar"] !== 'undefined' ? renderData.args["toolbar"] : true
  const sider = renderData && typeof renderData.args["sider"] !== 'undefined' ? renderData.args["sider"] : true

  return (
    <div style={{ width: '100%', height: `${HEIGHT}px`, border: "1px solid #d0d7de", borderRadius: "2px", ...cssStyle, display: 'flex' }}>
      <Layout style={{ flexDirection: 'row' }}>
        {sider &&
          <VTKViewerDrawer dispatch={viewerRef.current?.dispatch} viewerState={viewerState} handleScreenshot={handleScreenshot} />
        }
        <Layout>
          {toolbar &&
            <VTKFloatingToolbar dispatch={viewerRef.current?.dispatch} viewerState={viewerState} handleScreenshot={handleScreenshot} />
          }
          <Layout.Content style={{ display: 'flex', flexDirection: 'column' }}>
            <VTKViewer setViewerState={setViewerState} ref={viewerRef} />
          </Layout.Content>
        </Layout>
      </Layout>
    </div>
  )
}

export default VTKStreamlit