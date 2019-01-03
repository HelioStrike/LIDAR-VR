using System;
using System.IO;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PointCloudRenderer : MonoBehaviour {

	public int numX, numY, numZ;

	public string path;

	public string point2str(int i, int j, int k) {
		string str = "";
		int[] a = {i,j,k};

		for(int x = 0; x < 3; x++)
		{
			int b = a[x], c = 0;
			for(; b > 0; b = b/10)
			{
				c++;
			}

			for(int y = 0; y < 4-c; y++) { str += "0";}
			str += a[x].ToString();
		}

		return str;
	}

	// Use this for initialization
	void Start () {
		string[] lines = File.ReadAllLines(path);

		int inf = 99999999;
		float currX,currY,currZ,minX=inf,minY=inf,minZ=inf,maxX=-inf,maxY=-inf,maxZ=-inf;
		int totPoints = int.Parse(lines[1].Split(' ')[0]);

		int[,,] point_bins = new int[numX+1,numY+1,numZ+1];
		for(int i = 0; i < numX; i++)
		{
			for(int j = 0; j < numY; j++)
			{
				for(int k = 0; k < numZ; k++)
				{
					point_bins[i,j,k] = 0;
				}
			}
		}

		for(int i = 2; i < totPoints+2; i++)
		{
			string[] divs = lines[i].Split(' ');
			
			currX = float.Parse(divs[0]);
			currY = float.Parse(divs[1]);
			currZ = float.Parse(divs[2]);

			if(currX < minX) minX = currX;
			if(currX > maxX) maxX = currX;

			if(currY < minY) minY = currY;
			if(currY > maxY) maxY = currY;

			if(currZ < minZ) minZ = currZ;
			if(currZ > maxZ) maxZ = currZ;
		} 

		float diffX = Math.Abs(minX - maxX);
		float diffY = Math.Abs(minY - maxY);
		float diffZ = Math.Abs(minZ - maxZ);

		int numPoints = 0;
		for(int i = 2; i < totPoints+2; i++)
		{
			string[] divs = lines[i].Split(' ');
			
			currX = numX*(float.Parse(divs[0]) - minX)/diffX;
			currY = numY*(float.Parse(divs[1]) - minY)/diffY;
			currZ = numZ*(float.Parse(divs[2]) - minZ)/diffZ;

			if(point_bins[(int)currX,(int)currY,(int)currZ] == 0) { numPoints++;}
			point_bins[(int)currX,(int)currY,(int)currZ] = 1;
		} 

		int curr = 0;
		Vector3[] points = new Vector3[numPoints];
        Dictionary<string, int> point2index = new Dictionary<string, int>();
		
		for(int i = 0; i < numX; i++)
		{
			for(int j = 0; j < numY; j++)
			{
				for(int k = 0; k < numZ; k++)
				{
					if(point_bins[i,j,k] == 1)
					{
						string str = point2str(i,j,k);

						points[curr] = new Vector3(i*diffX/diffZ, j*diffY/diffZ, k);
						point2index.Add(str, curr);
						curr++;
					}
				}
			}
		}

		ArrayList tri = new ArrayList();
		int[] triangles;
		curr = 0;

		for(int i = 0; i < numX-2; i++)
		{
			for(int j = 0; j < numY-2; j++)
			{
				for(int k = 0; k < numZ-2; k++)
				{
					string[] strs = new string[8]; 
					for(int x = 0; x < 2; x++)
					{
						for(int y = 0; y < 2; y++)
						{
							for(int z = 0; z < 2; z++)
							{
								if(point_bins[i+x,j+y,k+z] == 1)
								{
									strs[x+2*y+4*z] = point2str(i+x, j+y, k+z);
								}
								else
								{
									strs[x+2*y+4*z] = "";
								}
							}
						}	
					}

					for(int x = 0; x < 8; x++)
					{
						for(int y = x+1; y < 8; y++)
						{
							for(int z = y+1; z < 8; z++)
							{
								if(strs[x] != "" && strs[y] != "" && strs[z] != "")
								{
									tri.Add(point2index[strs[x]]);
									tri.Add(point2index[strs[y]]);
									tri.Add(point2index[strs[z]]);
									curr += 3;
								}
							}
						}	
					}

				}
			}
		}

		triangles = new int[curr];
		curr = 0;
		foreach (var item in tri)
		{
			triangles[curr] = (int)item;
			curr++;
		}

		gameObject.AddComponent<MeshFilter>();
        gameObject.AddComponent<MeshRenderer>();
        Mesh mesh = GetComponent<MeshFilter>().mesh;

        mesh.Clear();

        mesh.vertices = points;
        mesh.triangles =  triangles;
	}
	
	// Update is called once per frame
	void Update () {
		
	}
}
