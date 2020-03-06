export type NodeInfo = {
  category: string
  type: string
  pid: number
  port: number
  protocols: string[]
  info: { [property: string]: any }
  services: string[]
}
