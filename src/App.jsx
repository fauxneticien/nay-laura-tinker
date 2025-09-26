import { useRef, useState, useMemo, useEffect } from 'react'
import { useWavesurfer } from '@wavesurfer/react'
import ZoomPlugin from 'wavesurfer.js/dist/plugins/zoom.esm.js'
import RegionsPlugin from 'wavesurfer.js/dist/plugins/regions.esm.js'
import jsonData from "../public/barackobamaunitednations65ARXE.json"

import './App.css';

const App = () => {
  const containerRef = useRef(null)
  const regionsPlugin = useMemo(() => RegionsPlugin.create(), []);
  const zoomPlugin = useMemo(() => ZoomPlugin.create(), []);
  const plugins = useMemo(() => [regionsPlugin, zoomPlugin], [regionsPlugin, zoomPlugin]);

  const { wavesurfer, isReady, isPlaying, currentTime } = useWavesurfer({
    container: containerRef,
    url: './barackobamaunitednations65ARXE.mp3',
    waveColor: 'purple',
    progressColor: 'purple',
    height: 100,
    plugins: plugins,
    dragToSeek: true,
    minPxPerSec: 100,
    backend: 'MediaElement',
  })

  const onPlayPause = () => {
    wavesurfer && wavesurfer.playPause()
  }


  useEffect(() => {
    if (isReady) {
      jsonData.timestamps.forEach((time) => {
        regionsPlugin.addRegion({
          //content: `TestRegion`,
          start: time.start,//wavesurfer.getCurrentTime(),
          end: time.end,//wavesurfer.getCurrentTime() + 300,
          drag: false,
          resize: true,
          color: "rgba(0, 255, 0, 0.1)"
        })
      })

    }
  }, [isReady])

  return (
    <div className="content bg-white scheme-light">
    <div className="flex-col items-center">
      <h1 className="text-3xl font-bold">Hello world!</h1>

      <div ref={containerRef} className="w-2/3 mx-auto"/>

      <button onClick={onPlayPause} className="btn btn-primary">
        {isPlaying ? 'Pause' : 'Play'}
      </button>
    </div>
    </div>
  );
};

export default App;
